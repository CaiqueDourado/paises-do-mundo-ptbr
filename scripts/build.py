"""Build the clean dataset from raw/paises_enriquecidos.csv.

Usage:  python scripts/build.py

Reads the raw export (kept untouched in raw/), applies the documented corrections
(docs/data-quality.md), renames columns to snake_case English, types every column and
writes data/paises.{csv,parquet,json} plus stats.json.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw" / "paises_enriquecidos.csv"
NAMES = ROOT / "corrections" / "nomes_pt_br.csv"
OUT = ROOT / "data"

# Corrections keyed by ISO alpha-2. Each one is listed in docs/data-quality.md.
FIXES: dict[str, dict[str, str]] = {
    "CL": {"macroContinente": "America", "continente": "South America"},
    "BA": {"macroContinente": "Europe", "continente": "Europe", "languages": "bos,hrv,srp"},
    "ZA": {"languages": "afr,eng,nbl,nso,sot,ssw,tsn,tso,ven,xho,zul"},
    "MS": {"languages": "eng"},
    "KG": {"languages": "kir,rus"},
    "MD": {"idiomas_oficiais_nomes": "Romanian"},
    "TJ": {"idioma_principal_corrigido": "tg", "locale_sugerido": "tg-TJ"},
    "TM": {"idioma_principal_corrigido": "tk", "locale_sugerido": "tk-TM"},
    "NO": {"locale_sugerido": "nb-NO"},
    "ZW": {"moeda_nome_pt": "Dólar americano, Ouro do Zimbábue (ZiG)"},
    "HK": {"idioma_principal_corrigido": "zh", "capital": ""},
    "MO": {"idioma_principal_corrigido": "zh"},
    "TW": {"idioma_principal_corrigido": "zh"},
    "MR": {
        "languages": "ara",
        "idiomas_oficiais_nomes": "Arabic",
        "direcao_escrita": "RTL",
    },
}

# Raw notes that only described an error which is now fixed are dropped (the error is
# documented in docs/data-quality.md); notes with lasting information are kept or reworded.
NOTES: dict[str, str] = {
    "CL": "",
    "BA": "",
    "SR": "",
    "IL": "",
    "MY": "",
    "DM": "",
    "MD": "",
    "MS": "Território Ultramarino Britânico.",
    "KG": "Quirguiz (ky) é o idioma estatal; russo é oficial.",
    "HK": "Região Administrativa Especial da China; não tem capital própria.",
    "MO": "Região Administrativa Especial da China; não tem capital própria.",
}

DIRECTION = {
    "LTR": "ltr",
    "RTL": "rtl",
    "RTL (com idioma oficial LTR)": "rtl",
    "LTR (com idioma oficial RTL)": "ltr",
}
SEPARATOR = {
    ",": "comma",
    ".": "period",
    " (espaço)": "space",
    " (espaço fino)": "narrow_space",
    "’": "apostrophe",
}
WEEKDAY = {"segunda": "monday", "domingo": "sunday", "sábado": "saturday"}
DRIVING = {"Direita": "right", "Esquerda": "left"}
MEASUREMENT = {
    "Métrico": "metric",
    "Métrico (com uso imperial)": "metric_with_imperial",
    "Imperial (EUA)/métrico": "us_customary_and_metric",
    "Imperial (EUA)": "us_customary",
}
YES_NO = {"Sim": True, "Não": False}


def split_list(value: str, sep: str = ",") -> str:
    """Normalises a comma separated list to a pipe separated one ("a|b|c")."""
    parts = [p.strip() for p in value.split(sep)]
    return "|".join(p for p in parts if p)


def load_raw() -> list[dict[str, str]]:
    with RAW.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    # Reviewed Brazilian Portuguese names (the raw export mixes pt-PT spellings and typos).
    with NAMES.open(encoding="utf-8", newline="") as handle:
        names = {r["iso2"]: r for r in csv.DictReader(handle)}
    for row in rows:
        iso2 = row["country_code_ISO_3166-1_alpha-2"]
        row.update(FIXES.get(iso2, {}))
        row["nome_pt"] = names[iso2]["name_pt"]
        row["nome_oficial_pt"] = names[iso2]["official_name_pt"]
        if iso2 in NOTES:
            row["observacoes_correcoes"] = NOTES[iso2]
    return rows


def transform(rows: list[dict[str, str]]) -> pd.DataFrame:
    out = []
    for r in rows:
        out.append(
            {
                "iso2": r["country_code_ISO_3166-1_alpha-2"],
                "iso3": r["country_code_3"],
                "iso_numeric": r["iso_numeric"],
                "ioc_code": r["codigo_coi"] or None,
                "name_en": r["pais"],
                "name_pt": r["nome_pt"],
                "official_name_pt": r["nome_oficial_pt"],
                "official_name_en": r["nome_oficial_en"],
                "native_name": r["nome_nativo"],
                "flag_emoji": r["bandeira_emoji"],
                "capital_en": r["capital"] or None,
                "continent_group": r["macroContinente"],
                "continent_subgroup": r["continente"],
                "un_region": r["regiao_onu"],
                "un_subregion": r["sub_regiao_onu"],
                "latitude": float(r["latitude"]),
                "longitude": float(r["longitude"]),
                "area_km2": int(r["area_km2"]),
                "population_millions": float(r["populacao_milhoes_aprox"]),
                "density_per_km2": float(r["densidade_hab_km2_aprox"]),
                "landlocked": YES_NO[r["sem_litoral"]],
                "borders_iso3": split_list(r["fronteiras_iso3"]) or None,
                "border_count": int(r["qtd_fronteiras"]),
                "independent": YES_NO[r["independente"]],
                "un_member": YES_NO[r["membro_onu"]],
                "government_pt": r["regime_politico"],
                "state_form_pt": r["forma_de_estado"],
                "memberships_pt": split_list(r["blocos_organizacoes"]) or None,
                "currency_codes": split_list(r["moeda_codigo"]),
                "currency_names_pt": split_list(r["moeda_nome_pt"]),
                "currency_symbols": split_list(r["moeda_simbolo"]),
                "primary_language": r["idioma_principal_corrigido"],
                "official_languages_iso639_2": split_list(r["languages"]),
                "official_languages_en": split_list(r["idiomas_oficiais_nomes"]),
                "locale": r["locale_sugerido"],
                "writing_direction": DIRECTION[r["direcao_escrita"]],
                "has_rtl_official_language": YES_NO[r["possui_idioma_rtl"]],
                "timezones_iana": split_list(r["fusos_iana"]),
                "utc_offset_count": int(r["qtd_fusos"]),
                "utc_offsets": r["utc_offset_padrao"],
                "observes_dst": YES_NO[r["horario_verao"]],
                "calling_code": r["ddi"],
                "cctld": split_list(r["tld"]),
                "demonym_en": r["gentilico_en"],
                "driving_side": DRIVING[r["mao_direcao"]],
                "first_day_of_week": WEEKDAY[r["primeiro_dia_semana"]],
                "time_format": r["formato_hora"],
                "short_date_pattern": r["formato_data_curto"].replace("‏", ""),
                "decimal_separator": SEPARATOR[r["separador_decimal"]],
                "grouping_separator": SEPARATOR[r["separador_milhar"]],
                "measurement_system": MEASUREMENT[r["sistema_medidas"]],
                "paper_size": r["tamanho_papel"],
                "notes_pt": r["observacoes_correcoes"] or None,
            }
        )
    frame = pd.DataFrame(out).sort_values("name_pt", key=lambda s: s.str.normalize("NFKD")).reset_index(drop=True)
    return frame


def stats(frame: pd.DataFrame) -> dict:
    columns = {}
    for name in frame.columns:
        series = frame[name]
        columns[name] = {
            "dtype": str(series.dtype),
            "non_null": int(series.notna().sum()),
            "null_pct": round(float(series.isna().mean() * 100), 2),
            "distinct": int(series.nunique(dropna=True)),
        }
    return {
        "dataset": "paises-do-mundo-ptbr",
        "rows": int(len(frame)),
        "columns": int(frame.shape[1]),
        "by_un_region": frame["un_region"].value_counts().sort_index().to_dict(),
        "fields": columns,
    }


def main() -> None:
    frame = transform(load_raw())
    OUT.mkdir(exist_ok=True)
    frame.to_csv(OUT / "paises.csv", index=False, encoding="utf-8", lineterminator="\n")
    frame.to_parquet(OUT / "paises.parquet", index=False)
    records = json.loads(frame.to_json(orient="records", force_ascii=False))
    (OUT / "paises.json").write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ROOT / "stats.json").write_text(json.dumps(stats(frame), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{len(frame)} rows, {frame.shape[1]} columns -> data/")


if __name__ == "__main__":
    main()
