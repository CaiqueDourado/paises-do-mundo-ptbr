# Países do mundo (pt-BR)

[![validate](https://github.com/CaiqueDourado/paises-do-mundo-ptbr/actions/workflows/validate.yml/badge.svg)](https://github.com/CaiqueDourado/paises-do-mundo-ptbr/actions/workflows/validate.yml)
[![Dados: CC BY 4.0](https://img.shields.io/badge/dados-CC%20BY%204.0-lightgrey.svg)](LICENSE-DATA.md)
[![Código: MIT](https://img.shields.io/badge/c%C3%B3digo-MIT-blue.svg)](LICENSE)
[![Kaggle](https://img.shields.io/badge/Kaggle-dataset-20BEFF.svg)](https://www.kaggle.com/datasets/caiquedourado/paises-do-mundo-ptbr)

**Países do mundo com códigos ISO, nomes em português do Brasil, idiomas, moedas, fusos horários e formatos regionais.** 167 países e territórios, 53 colunas tipadas, em CSV, Parquet e JSON.

[Read in English](README.md)

Feito para quem precisa localizar software: qual locale usar, como formatar datas e números, qual moeda e DDI valem, em que dia a semana começa, se o texto corre da direita para a esquerda.

## Prévia

| iso2 | | name_pt | capital_en | moeda | locale | semana começa | data curta | decimal | direção | fusos IANA |
|---|---|---|---|---|---|---|---|---|---|---|
| BR | 🇧🇷 | Brasil | Brasília | BRL | pt-BR | sunday | dd/MM/y | comma | ltr | 16 |
| PT | 🇵🇹 | Portugal | Lisbon | EUR | pt-PT | sunday | dd/MM/yy | comma | ltr | 3 |
| JP | 🇯🇵 | Japão | Tokyo | JPY | ja-JP | sunday | y/MM/dd | period | ltr | 1 |
| SA | 🇸🇦 | Arábia Saudita | Riyadh | SAR | ar-SA | sunday | d/M/y | period | rtl | 1 |
| US | 🇺🇸 | Estados Unidos | Washington D.C. | USD | en-US | sunday | M/d/yy | period | ltr | 29 |

## Como usar

```python
import pandas as pd

url = "https://raw.githubusercontent.com/CaiqueDourado/paises-do-mundo-ptbr/main/data/paises.csv"
df = pd.read_csv(url, keep_default_na=False, dtype={"iso_numeric": str})

df[df.primary_language == "pt"][["flag_emoji", "name_pt", "currency_codes", "locale"]]
```

O arquivo Parquet já vem tipado (booleanos, inteiros, decimais) e pode ser consultado direto no DuckDB:

```sql
SELECT un_region, count(*) AS paises FROM 'data/paises.parquet' GROUP BY un_region;
```

## O que tem

Códigos (ISO, COI, DDI, domínios), nomes (português, inglês, nativo, bandeira, capital, gentílico), geografia (região da ONU, coordenadas, área, população, fronteiras), política (independência, ONU, regime, blocos), moedas, idiomas e formatos regionais (locale, direção da escrita, primeiro dia da semana, relógio 12/24h, padrão de data, separadores, sistema de medidas, papel) e fusos horários.

Cada coluna está descrita no **[dicionário de dados](docs/data-dictionary.pt-BR.md)**, com tipo, percentual de nulos, exemplo, padrão de referência e origem.

## Como foi construído

A lista de países nasceu no **[919Apps](https://web.archive.org/web/20211203115104/https://919apps.com/lca/download-app-mhs-schedule)** (2021), um catálogo programático de 2,4 milhões de apps gerado a partir do Apple Enterprise Partner Feed e localizado para cada loja da App Store com `CultureInfo` e `RegionInfo` do .NET. Por isso são 167 entradas: as lojas da App Store, e não todos os países do mundo.

[![919Apps](https://raw.githubusercontent.com/CaiqueDourado/CaiqueDourado/main/assets/919apps.com_screenshot.png)](https://web.archive.org/web/20211203115104/https://919apps.com/lca/download-app-mhs-schedule)

*919Apps, [versão arquivada no Wayback Machine](https://web.archive.org/web/20211203115104/https://919apps.com/lca/download-app-mhs-schedule).*

Em 2026 a tabela foi enriquecida seguindo ISO 3166, ISO 4217, ISO 639, ONU M49, Unicode CLDR e a base de fusos IANA, e depois perfilada, corrigida e validada. Detalhes em [methodology.md](docs/methodology.md) (em inglês).

## Qualidade

O perfil da exportação original encontrou 18 tipos de problema. Alguns exemplos:

- Chile classificado como Oceania.
- Listas ISO 639-2 com cree e somali por engano.
- Idioma da Malásia codificado como birmanês.
- Nomes em português de Portugal (`Quénia`, `Vietname`).
- Marcas invisíveis de direção dentro dos padrões de data.

Toda correção é código (`scripts/build.py`), o arquivo original fica em `raw/` e `scripts/validate.py` protege o resultado no CI. A lista completa e as limitações conhecidas estão em [data-quality.md](docs/data-quality.md).

## Reconstruir

```bash
pip install -r requirements.txt
python scripts/build.py && python scripts/validate.py && python scripts/docs.py
```

## Licença

Dados: [CC BY 4.0](LICENSE-DATA.md). Código: [MIT](LICENSE). Como citar: [CITATION.cff](CITATION.cff).

Achou um erro? Abra uma issue com o país e a coluna.

## Autor

**Caique Dourado**: 20 anos construindo crawlers, pipelines de dados e SEO programático em .NET e SQL Server. Outros datasets e bibliotecas em [github.com/CaiqueDourado](https://github.com/CaiqueDourado), como a [PtBr.Text](https://github.com/CaiqueDourado/PtBr.Text) (utilitários de texto em português) e o [BrCommerceKit](https://github.com/CaiqueDourado/BrCommerceKit). Do mesmo projeto: [brazilian-ecommerce-products](https://github.com/CaiqueDourado/brazilian-ecommerce-products), 114,6 milhões de ofertas de lojas brasileiras.
