# Data quality report

What was found while profiling the raw export, and what was done about it. Every fix lives in `scripts/build.py` (`FIXES`, `NOTES`); `raw/` keeps the original values for comparison.

## Fixed in the clean version

| # | Problem in `raw/` | Rows | Fix |
|---|---|---|---|
| 1 | Chile classified as `Oceania` (because of Easter Island) | CL | `continent_group` = America, `continent_subgroup` = South America |
| 2 | `Europa` instead of `Europe`, unlike every other row | BA | Normalised to `Europe` |
| 3 | `inicial` identical to `continente` in all rows | all | Column dropped |
| 4 | Wrong main language in the original `language` column: `sr` (Serbian) for Suriname, `my` (Burmese) for Malaysia, `es` for Dominica, `ms` (Malay) for Montserrat, `ru` for Moldova, `en` for Israel, `zh` for Singapore | SR, MY, DM, MS, MD, IL, SG | `primary_language` uses the corrected value (`nl`, `ms`, `en`, `en`, `ro`, `he`, `en`); the original column is dropped |
| 5 | ISO 639-2 list with codes of unrelated languages: `cre` (Cree) for Croatian in Bosnia, `som` (Somali) in South Africa | BA, ZA | `bos,hrv,srp`; South Africa's 11 official languages |
| 6 | Empty language list; Kyrgyz missing | MS, KG | `eng`; `kir,rus` |
| 7 | French listed as official in Mauritania (only Arabic is) and direction "RTL with LTR official language" | MR | `ara`, `rtl` |
| 8 | "Moldavian" as language name | MD | `Romanian` (official name since 2023) |
| 9 | Russian as main language where the state language is another one; locale without region (`ru`) | TJ, TM | `tg` / `tg-TJ`, `tk` / `tk-TM` |
| 10 | Locale `no` without region | NO | `nb-NO` |
| 11 | `zh-TW` (a locale, and Taiwan's) used as language code for Hong Kong and Macau | HK, MO, TW | `primary_language` = `zh`; the locale keeps the script and region (`zh-Hant-HK`) |
| 12 | Hong Kong with capital "City of Victoria"; Macau with empty capital | HK, MO | Both empty, with a note: special administrative regions have no capital |
| 13 | Currency name `ZWG` instead of a name | ZW | `Ouro do Zimbábue (ZiG)` |
| 14 | Invisible right-to-left marks (U+200F) inside date patterns | 16 Arabic-locale rows | Removed |
| 15 | Thousands separator stored as prose: `" (espaço)"`, `" (espaço fino)"` | 42 | Enumeration: `space` (U+00A0), `narrow_space` (U+202F) |
| 16 | Yes/no as `Sim`/`Não`, lists as comma separated text | all | Booleans; lists separated by `|` |
| 17 | Portuguese names mixed European Portuguese spellings (`Quénia`, `Polónia`, `Vietname`, `Madagáscar`), outdated or non-Brazilian forms (`Holanda`, `Ilha Formosa`, `Suazilândia`, `Ilhas Caimão`), typos (`Azerbeijão`, `São Vincente`, `Perú`, `República português`, `nova Zelândia`, `Co -operative República da Guiana`) and untranslated values (`Georgia`, `Grenada`) | 31 names, 49 official names | Replaced by the reviewed table `corrections/nomes_pt_br.csv` (Brazilian usage, Itamaraty forms) |
| 18 | Notes that only described one of the errors above | 7 dropped, 4 reworded | Dropped from or reworded in `notes_pt` (the error is documented here) |

## Known limitations (kept as they are)

- **Coverage:** 167 App Store storefronts, not all countries of the world. Territories such as Bermuda and Hong Kong are included; Cuba, Iran, North Korea and Syria are not.
- **`name_en`** keeps the App Store naming (`Swaziland`, `Turkey`, `Czech Republic`, `Cote D'Ivoire`). Current official names are in `official_name_en` and `notes_pt`.
- **`continent_group`** mixes continents with sub-regions (`Caribbean`, `Melanesia`, `Australia`) because it mirrored the site's home page. Use `un_region` for analysis.
- **Population, area and coordinates** are approximate (circa 2024–2025; coordinates are rough centres, often integers). They are fine for maps and rankings, not for official statistics.
- **`utc_offset_count`** counts distinct standard offsets, not IANA zones: Argentina has 1 offset and 12 zones.
- **`observes_dst`** is true when any part of the country observes daylight saving time (Mexico: only the northern border zones since 2022).
- **Political fields** (`government_pt`, `memberships_pt`, currency changes such as Bulgaria adopting the euro in 2026) reflect October 2026 and will age.
- **`borders_iso3`** can reference countries outside the dataset, and uses `UNK` for Kosovo (not an ISO code).

## Automated checks

`scripts/validate.py` runs on every push (GitHub Actions) and fails the build if any of these break: row count, unique and well-formed ISO codes, locale format and region, enumerations, booleans, coordinate ranges, border symmetry and count, density vs. population/area, RTL consistency, and leftover invisible characters or padding spaces.
