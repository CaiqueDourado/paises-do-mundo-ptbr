# Países do mundo (pt-BR) · Countries of the world

[![validate](https://github.com/CaiqueDourado/paises-do-mundo-ptbr/actions/workflows/validate.yml/badge.svg)](https://github.com/CaiqueDourado/paises-do-mundo-ptbr/actions/workflows/validate.yml)
[![Data: CC BY 4.0](https://img.shields.io/badge/data-CC%20BY%204.0-lightgrey.svg)](LICENSE-DATA.md)
[![Code: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)
[![Kaggle](https://img.shields.io/badge/Kaggle-dataset-20BEFF.svg)](https://www.kaggle.com/datasets/caiquedourado/paises-do-mundo-ptbr)

**pt-BR:** Países do mundo com códigos ISO, nomes em português do Brasil, idiomas, moedas, fusos horários e formatos regionais. 167 países e territórios, 53 colunas.
**en:** Countries of the world with ISO codes, Brazilian Portuguese names, languages, currencies, time zones and locale formats. 167 countries and territories, 53 columns.

[Leia em português](README.pt-BR.md)

| Rows | Columns | Formats | Size | Checks |
|---|---|---|---|---|
| 167 | 53, typed | CSV · Parquet · JSON | < 500 KB | validated in CI on every push |

## Preview

| iso2 | | name_pt | capital_en | currency | locale | week starts | short date | decimal | direction | IANA zones |
|---|---|---|---|---|---|---|---|---|---|---|
| BR | 🇧🇷 | Brasil | Brasília | BRL | pt-BR | sunday | dd/MM/y | comma | ltr | 16 |
| PT | 🇵🇹 | Portugal | Lisbon | EUR | pt-PT | sunday | dd/MM/yy | comma | ltr | 3 |
| JP | 🇯🇵 | Japão | Tokyo | JPY | ja-JP | sunday | y/MM/dd | period | ltr | 1 |
| SA | 🇸🇦 | Arábia Saudita | Riyadh | SAR | ar-SA | sunday | d/M/y | period | rtl | 1 |
| US | 🇺🇸 | Estados Unidos | Washington D.C. | USD | en-US | sunday | M/d/yy | period | ltr | 29 |

## Use it

```python
import pandas as pd

url = "https://raw.githubusercontent.com/CaiqueDourado/paises-do-mundo-ptbr/main/data/paises.csv"
df = pd.read_csv(url, keep_default_na=False, dtype={"iso_numeric": str})

df[df.primary_language == "pt"][["flag_emoji", "name_pt", "currency_codes", "locale"]]
```

```sql
-- DuckDB reads the Parquet file directly, with types
SELECT un_region, count(*) AS countries, round(sum(population_millions)) AS population_m
FROM 'data/paises.parquet'
GROUP BY un_region ORDER BY population_m DESC;
```

## What is inside

| Group | Columns |
|---|---|
| Codes | `iso2`, `iso3`, `iso_numeric`, `ioc_code`, `calling_code`, `cctld` |
| Names | `name_pt`, `official_name_pt`, `name_en`, `official_name_en`, `native_name`, `flag_emoji`, `capital_en`, `demonym_en` |
| Geography | `un_region`, `un_subregion`, `continent_group`, `continent_subgroup`, `latitude`, `longitude`, `area_km2`, `population_millions`, `density_per_km2`, `landlocked`, `borders_iso3`, `border_count` |
| Politics | `independent`, `un_member`, `government_pt`, `state_form_pt`, `memberships_pt` |
| Money | `currency_codes`, `currency_names_pt`, `currency_symbols` |
| Language and locale | `primary_language`, `official_languages_iso639_2`, `official_languages_en`, `locale`, `writing_direction`, `has_rtl_official_language`, `first_day_of_week`, `time_format`, `short_date_pattern`, `decimal_separator`, `grouping_separator`, `measurement_system`, `paper_size` |
| Time | `timezones_iana`, `utc_offset_count`, `utc_offsets`, `observes_dst` |
| Notes | `notes_pt` |

Every column is described in the **[data dictionary](docs/data-dictionary.md)** ([pt-BR](docs/data-dictionary.pt-BR.md)), with type, null rate, example, standard and origin.

## How it was built

The country list was born in **[919Apps](https://web.archive.org/web/20211203115104/https://919apps.com/lca/download-app-mhs-schedule)** (2021), a programmatic catalog of 2.4 million apps generated from the Apple Enterprise Partner Feed and localised for every App Store storefront with .NET `CultureInfo` and `RegionInfo`. That is why it has 167 entries: the storefronts, not every country in the world.

[![919Apps](https://raw.githubusercontent.com/CaiqueDourado/CaiqueDourado/main/assets/919apps.com_screenshot.png)](https://web.archive.org/web/20211203115104/https://919apps.com/lca/download-app-mhs-schedule)

*919Apps, [archived on the Wayback Machine](https://web.archive.org/web/20211203115104/https://919apps.com/lca/download-app-mhs-schedule).*

In 2026 the table was enriched following ISO 3166, ISO 4217, ISO 639, UN M49, Unicode CLDR and the IANA time zone database, then profiled, corrected and validated. Details in [methodology](docs/methodology.md).

## Data quality

Profiling the raw export found 18 classes of problems. Among them: Chile classified as Oceania, ISO 639-2 lists containing Cree and Somali by mistake, Malaysia's language coded as Burmese, Portuguese names in European spelling (`Quénia`, `Vietname`), and invisible right-to-left marks inside date patterns. Every fix is code (`scripts/build.py`), the raw file is kept in `raw/`, and `scripts/validate.py` guards the result in CI. Full list and known limitations: [data-quality.md](docs/data-quality.md).

## Repository layout

```text
data/          clean dataset: paises.csv, paises.parquet, paises.json, dataset-metadata.json (Kaggle)
raw/           original export, untouched
corrections/   reviewed tables applied by the build (Brazilian Portuguese names)
schema/        column definitions and dataset metadata: the single source for docs and Kaggle
scripts/       build.py (raw → clean), validate.py (checks), docs.py (dictionaries + Kaggle metadata)
notebooks/     eda.ipynb, exploratory analysis
docs/          data dictionary, methodology, data quality
stats.json     row count and per-column coverage, generated
```

Rebuild everything:

```bash
pip install -r requirements.txt
python scripts/build.py && python scripts/validate.py && python scripts/docs.py
```

## License

Data: [CC BY 4.0](LICENSE-DATA.md). Code: [MIT](LICENSE). Please cite as described in [CITATION.cff](CITATION.cff).

Found an error? Open an issue with the country and the column.

## Author

**Caique Dourado**: 20 years building crawlers, data pipelines and programmatic SEO in .NET and SQL Server. More datasets and libraries at [github.com/CaiqueDourado](https://github.com/CaiqueDourado), including [PtBr.Text](https://github.com/CaiqueDourado/PtBr.Text) (Brazilian Portuguese text utilities) and [BrCommerceKit](https://github.com/CaiqueDourado/BrCommerceKit). Same project: [catalogo-produtos-ecommerce-brasil](https://github.com/CaiqueDourado/catalogo-produtos-ecommerce-brasil), 114.6 million offers from Brazilian online stores.
