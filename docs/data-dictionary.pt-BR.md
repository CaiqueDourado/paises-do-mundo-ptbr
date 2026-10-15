# Dicionário de dados: Países do mundo: códigos, idiomas, moedas, fusos e formatos regionais

Gerado por `scripts/docs.py` a partir de `schema/columns.json`. Tipos, nulos e exemplos vêm dos arquivos em `data/`.

## `paises.csv`

Uma linha por país ou território (167): códigos, nomes em português e inglês, regiões, fronteiras, moedas, idiomas, formatos regionais e fusos horários.

| Coluna | Tipo | Nulos | Exemplo | Descrição | Padrão | Origem |
|---|---|---|---|---|---|---|
| `iso2` | string | 0,0% | `IN` | Código ISO 3166-1 alfa-2. Chave primária. | ISO 3166-1 | 919Apps |
| `iso3` | string | 0,0% | `IND` | Código ISO 3166-1 alfa-3. | ISO 3166-1 | 919Apps |
| `iso_numeric` | string | 0,0% | `356` | Código numérico ISO 3166-1, como texto para manter os zeros à esquerda ("024"). | ISO 3166-1 | enriquecimento |
| `ioc_code` | string | 2,4% | `IND` | Código do Comitê Olímpico Internacional. Vazio em territórios sem comitê olímpico próprio. | IOC | enriquecimento |
| `name_en` | string | 0,0% | `India` | Nome curto em inglês como aparece na lista de lojas da App Store (ex.: "Swaziland", "Korea, Republic Of"). | — | 919Apps |
| `name_pt` | string | 0,0% | `Índia` | Nome usual em português do Brasil. | — | enriquecimento |
| `official_name_pt` | string | 0,0% | `República da Índia` | Nome oficial completo em português. | — | enriquecimento |
| `official_name_en` | string | 0,0% | `Republic of India` | Nome oficial completo em inglês. | — | enriquecimento |
| `native_name` | string | 0,0% | `India / भारत / இந்தியா` | Nome no idioma e na escrita oficiais principais. | — | enriquecimento |
| `flag_emoji` | string | 0,0% | `🇮🇳` | Emoji da bandeira (par de indicadores regionais). | Unicode | enriquecimento |
| `capital_en` | string | 1,2% | `New Delhi` | Capital em inglês. Mais de uma capital vem separada por ", " (África do Sul). Vazio para Hong Kong e Macau. | — | enriquecimento |
| `continent_group` | string | 0,0% | `Asia` | Agrupamento usado na home do 919Apps (Africa, America, Asia, Caribbean, Europe, Oceania…). Mantido por compatibilidade; para análise, prefira un_region. | — | 919Apps |
| `continent_subgroup` | string | 0,0% | `Southern Asia` | Subagrupamento usado na home do 919Apps (South America, Eastern Europe…). | — | 919Apps |
| `un_region` | string | 0,0% | `Asia` | Região da ONU (M49): Africa, Americas, Asia, Europe, Oceania. | UN M49 | enriquecimento |
| `un_subregion` | string | 0,0% | `Southern Asia` | Sub-região da ONU (M49), ex.: Western Africa, South America. | UN M49 | enriquecimento |
| `latitude` | float | 0,0% | `20.0` | Latitude aproximada do centro do país, em graus decimais. | WGS 84 | enriquecimento |
| `longitude` | float | 0,0% | `77.0` | Longitude aproximada do centro do país, em graus decimais. | WGS 84 | enriquecimento |
| `area_km2` | integer | 0,0% | `3287590` | Área total em km². | — | enriquecimento |
| `population_millions` | float | 0,0% | `1450.9` | População aproximada em milhões, cerca de 2024–2025. | — | enriquecimento |
| `density_per_km2` | float | 0,0% | `441.3` | Habitantes por km², aproximado (população / área). | — | enriquecimento |
| `landlocked` | boolean | 0,0% | `False` | Verdadeiro quando o país não tem litoral. | — | enriquecimento |
| `borders_iso3` | string (list) | 22,8% | `AUT\|FRA\|SMR\|SVN\|CHE\|VAT` | Vizinhos por terra em códigos ISO alfa-3 separados por "\|". Pode citar países fora desta base; UNK = Kosovo. | ISO 3166-1 | enriquecimento |
| `border_count` | integer | 0,0% | `6` | Quantidade de vizinhos por terra (tamanho de borders_iso3). | — | enriquecimento |
| `independent` | boolean | 0,0% | `True` | Verdadeiro para Estados soberanos; falso para dependências e regiões administrativas especiais. | — | enriquecimento |
| `un_member` | boolean | 0,0% | `True` | Verdadeiro para membros da ONU. | — | enriquecimento |
| `government_pt` | string | 0,0% | `República parlamentarista` | Regime político, em português. | — | enriquecimento |
| `state_form_pt` | string | 0,0% | `Federal` | Forma de Estado (Unitário, Federal, Dependência…). | — | enriquecimento |
| `memberships_pt` | string (list) | 20,4% | `UE\|Zona do Euro\|Schengen\|OTAN\|G20\|OCDE` | Blocos e organizações, separados por "\|" (UE, Mercosul, OTAN, G20…). | — | enriquecimento |
| `currency_codes` | string (list) | 0,0% | `INR` | Códigos ISO 4217 das moedas em uso, separados por "\|". | ISO 4217 | enriquecimento |
| `currency_names_pt` | string (list) | 0,0% | `Rupia indiana` | Nomes das moedas em português, na mesma ordem de currency_codes. | — | enriquecimento |
| `currency_symbols` | string (list) | 0,0% | `₹` | Símbolos locais das moedas, na mesma ordem de currency_codes. | CLDR | enriquecimento |
| `primary_language` | string | 0,0% | `hi` | Idioma principal, ISO 639-1 (ou 639-3 quando não existe código de duas letras). | ISO 639 | 919Apps, corrigido |
| `official_languages_iso639_2` | string (list) | 0,0% | `eng\|hin` | Idiomas oficiais em códigos ISO 639-2/B, separados por "\|". | ISO 639-2 | 919Apps, corrigido |
| `official_languages_en` | string (list) | 0,0% | `English\|Hindi\|Tamil` | Idiomas oficiais e reconhecidos, com nomes em inglês, separados por "\|". | — | enriquecimento |
| `locale` | string | 0,0% | `hi-IN` | Locale BCP 47 sugerido para o país (pt-BR, zh-Hant-HK…). | BCP 47 / CLDR | enriquecimento |
| `writing_direction` | string | 0,0% | `ltr` | Direção da escrita do idioma principal: ltr ou rtl. | CLDR | enriquecimento |
| `has_rtl_official_language` | boolean | 0,0% | `False` | Verdadeiro quando ao menos um idioma oficial é escrito da direita para a esquerda. | CLDR | enriquecimento |
| `timezones_iana` | string (list) | 0,0% | `Asia/Kolkata` | Identificadores de fuso IANA, separados por "\|". | IANA tzdb | enriquecimento |
| `utc_offset_count` | integer | 0,0% | `1` | Quantidade de deslocamentos UTC padrão distintos (não é a quantidade de fusos IANA). | — | enriquecimento |
| `utc_offsets` | string | 0,0% | `UTC+05:30` | Deslocamento padrão, ou intervalo "UTC-05:00 a UTC-02:00" quando há vários. | — | enriquecimento |
| `observes_dst` | boolean | 0,0% | `False` | Verdadeiro quando há horário de verão em ao menos parte do país. | IANA tzdb | enriquecimento |
| `calling_code` | string | 0,0% | `+91` | Código telefônico internacional (+55). | ITU-T E.164 | enriquecimento |
| `cctld` | string (list) | 0,0% | `.in` | Domínios de topo do país, inclusive os internacionalizados, separados por "\|". | IANA root zone | enriquecimento |
| `demonym_en` | string | 0,0% | `Indian` | Gentílico em inglês. | — | enriquecimento |
| `driving_side` | string | 0,0% | `left` | Mão de direção: right (direita) ou left (esquerda). | — | enriquecimento |
| `first_day_of_week` | string | 0,0% | `sunday` | Primeiro dia da semana nos calendários: monday, sunday ou saturday. | CLDR | enriquecimento |
| `time_format` | string | 0,0% | `12h` | Relógio usual: 12h ou 24h. | CLDR | enriquecimento |
| `short_date_pattern` | string | 0,0% | `d/M/yy` | Padrão de data curta do locale (dd/MM/y). | CLDR | enriquecimento |
| `decimal_separator` | string | 0,0% | `period` | Separador decimal: comma (vírgula) ou period (ponto). | CLDR | enriquecimento |
| `grouping_separator` | string | 0,0% | `comma` | Separador de milhar: comma, period, space (U+00A0), narrow_space (U+202F) ou apostrophe (’). | CLDR | enriquecimento |
| `measurement_system` | string | 0,0% | `metric` | metric, metric_with_imperial, us_customary_and_metric ou us_customary. | CLDR | enriquecimento |
| `paper_size` | string | 0,0% | `A4` | Tamanho de papel padrão: A4 ou Letter. | CLDR | enriquecimento |
| `notes_pt` | string | 83,8% | `Território Ultramarino Britânico.` | Observações em português (status político, geografia, mudanças recentes). | — | enriquecimento |

## Convenções

- Codificação UTF-8 sem BOM, separador vírgula, cabeçalho na primeira linha, quebra de linha `\n`.
- Listas dentro de uma célula usam `|` como separador (`MNE|GRC|MKD`). Vírgula nunca separa itens.
- Booleanos são `True` / `False`. Célula vazia = desconhecido ou não se aplica.
- Separador decimal é o ponto `.`, sem separador de milhar.
- Textos para leitura estão em português (`*_pt`); enumerações técnicas são códigos em inglês minúsculo (`ltr`, `monday`).
