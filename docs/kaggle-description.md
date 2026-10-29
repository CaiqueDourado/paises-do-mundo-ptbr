**Países do mundo** com códigos, nomes em português, idiomas, moedas, fusos horários e formatos regionais. **Countries of the world** with ISO codes, Portuguese names, languages, currencies, time zones and locale formats.

167 countries and territories × 53 typed columns, built for software that needs to localise content: which locale to use, how to format dates and numbers, which currency and calling code apply, which day starts the week, whether text runs right to left.

## What is inside

- **Codes:** ISO 3166-1 alpha-2, alpha-3 and numeric, IOC code, calling code, ccTLDs (including internationalised ones).
- **Names:** Brazilian Portuguese common and official names, English official name, native name, flag emoji, capital, demonym.
- **Geography:** UN M49 region and sub-region, approximate centre, area, population (circa 2024–2025), density, landlocked flag, land borders.
- **Politics:** independence, UN membership, system of government, form of state, blocs (EU, Mercosur, NATO, G20…).
- **Languages and locale:** main language, official languages, BCP 47 locale, writing direction, first day of the week, 12/24h clock, short date pattern, decimal and thousands separators, measurement system, paper size.
- **Time:** IANA time zones, number of UTC offsets, daylight saving time.
- **Money:** ISO 4217 codes, names in Portuguese, symbols.

## Files

- `paises.csv`: UTF-8, comma separated; lists inside a cell use `|`.
- `paises.parquet`: same data with types (booleans, integers, floats).
- `paises.json`: array of records.

## How a country is structured

![Brazil as one nested JSON record](https://raw.githubusercontent.com/CaiqueDourado/paises-do-mundo-ptbr/main/docs/img/country-json.png)

Each row is flat (53 columns), but the columns fall into groups. The record above is Brazil regrouped that way: codes, names, geography, politics, money, locale and time, with the `|` lists split and each of its 10 land borders joined back to its own row to get the Portuguese name. Brazil has 211.9 million people on 8,515,767 km², one currency (BRL, R$) and 16 IANA time zones over 4 UTC offsets. Full record: [docs/example-country.json](https://github.com/CaiqueDourado/paises-do-mundo-ptbr/blob/main/docs/example-country.json), built by [scripts/make_json.py](https://github.com/CaiqueDourado/paises-do-mundo-ptbr/blob/main/scripts/make_json.py).

## Origin and quality

The country list comes from [919Apps](https://web.archive.org/web/20211203115104/https://919apps.com/lca/download-app-mhs-schedule), a 2021 App Store catalog by the author (167 storefronts). It was enriched following ISO, UN M49, Unicode CLDR and IANA standards, then validated: ISO codes, border symmetry, density, locale consistency. Eighteen classes of errors found in the original data were fixed and documented.

Full data dictionary, methodology, quality report and the build/validation scripts: **https://github.com/CaiqueDourado/paises-do-mundo-ptbr**

License: CC BY 4.0. Author: Caique Dourado.

Same project: Brazilian e-commerce product catalog, 114.6 million offers from 7,179 stores: https://www.kaggle.com/datasets/caiquedourado/catalogo-produtos-ecommerce-brasil
