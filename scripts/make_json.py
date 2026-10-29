"""Build one country as a nested JSON record (docs/example-country.json), for the README and Kaggle.

    python scripts/make_json.py          # Brazil
    python scripts/make_json.py JP       # any iso2 code

Reads data/paises.json, groups the 53 flat columns the same way as the README (codes, names, geography,
politics, money, language and locale, time), splits the `|` lists and joins each land border back to its
own row in the same table to get the Portuguese name. Only the standard library is needed.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = "BR"


def split(value: str | None) -> list[str]:
    return value.split("|") if value else []


def build(rows: list[dict], iso2: str) -> dict:
    by_iso3 = {r["iso3"]: r for r in rows}
    c = next(r for r in rows if r["iso2"] == iso2)
    currencies = [
        {"code": code, "name_pt": name, "symbol": symbol}
        for code, name, symbol in zip(split(c["currency_codes"]), split(c["currency_names_pt"]), split(c["currency_symbols"]))
    ]
    languages = [
        {"iso639_2": code, "name_en": name}
        for code, name in zip(split(c["official_languages_iso639_2"]), split(c["official_languages_en"]))
    ]
    borders = [{"iso3": b, "name_pt": by_iso3[b]["name_pt"] if b in by_iso3 else None} for b in split(c["borders_iso3"])]
    return {
        "iso2": c["iso2"],
        "flag_emoji": c["flag_emoji"],
        "names": {
            "pt": c["name_pt"],
            "official_pt": c["official_name_pt"],
            "en": c["name_en"],
            "official_en": c["official_name_en"],
            "native": c["native_name"],
            "capital_en": c["capital_en"],
            "demonym_en": c["demonym_en"],
        },
        "codes": {
            "iso2": c["iso2"],
            "iso3": c["iso3"],
            "iso_numeric": c["iso_numeric"],
            "ioc": c["ioc_code"],
            "calling_code": c["calling_code"],
            "cctld": split(c["cctld"]),
        },
        "geography": {
            "un_region": c["un_region"],
            "un_subregion": c["un_subregion"],
            "continent_group": c["continent_group"],
            "continent_subgroup": c["continent_subgroup"],
            "center": {"latitude": c["latitude"], "longitude": c["longitude"]},
            "area_km2": c["area_km2"],
            "population_millions": c["population_millions"],
            "density_per_km2": c["density_per_km2"],
            "landlocked": c["landlocked"],
            "border_count": c["border_count"],
            "borders": borders,
        },
        "politics": {
            "independent": c["independent"],
            "un_member": c["un_member"],
            "government_pt": c["government_pt"],
            "state_form_pt": c["state_form_pt"],
            "memberships_pt": split(c["memberships_pt"]),
        },
        "money": {"currencies": currencies},
        "language_and_locale": {
            "primary_language": c["primary_language"],
            "official_languages": languages,
            "locale": c["locale"],
            "writing_direction": c["writing_direction"],
            "has_rtl_official_language": c["has_rtl_official_language"],
            "formats": {
                "first_day_of_week": c["first_day_of_week"],
                "time_format": c["time_format"],
                "short_date_pattern": c["short_date_pattern"],
                "decimal_separator": c["decimal_separator"],
                "grouping_separator": c["grouping_separator"],
                "measurement_system": c["measurement_system"],
                "paper_size": c["paper_size"],
                "driving_side": c["driving_side"],
            },
        },
        "time": {
            "timezones_iana": split(c["timezones_iana"]),
            "utc_offset_count": c["utc_offset_count"],
            "utc_offsets": c["utc_offsets"],
            "observes_dst": c["observes_dst"],
        },
        "notes_pt": c["notes_pt"],
    }


def main() -> None:
    iso2 = (sys.argv[1] if len(sys.argv) > 1 else DEFAULT).upper()
    rows = json.loads((ROOT / "data" / "paises.json").read_text(encoding="utf-8"))
    out = ROOT / "docs" / "example-country.json"
    out.write_text(json.dumps(build(rows, iso2), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
