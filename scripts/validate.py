"""Validate data/paises.csv. Exits with code 1 and lists every failure.

Usage:  python scripts/validate.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
failures: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


def main() -> int:
    frame = pd.read_csv(ROOT / "data" / "paises.csv", dtype=str, keep_default_na=False)
    parquet = pd.read_parquet(ROOT / "data" / "paises.parquet")

    check(len(frame) == 167, f"expected 167 rows, got {len(frame)}")
    check(len(parquet) == len(frame), "CSV and Parquet have different row counts")
    check(list(parquet.columns) == list(frame.columns), "CSV and Parquet have different columns")

    for column, pattern in {
        "iso2": r"[A-Z]{2}",
        "iso3": r"[A-Z]{3}",
        "iso_numeric": r"\d{3}",
        "calling_code": r"\+\d{1,4}",
        "locale": r"[a-z]{2,3}(-[A-Z][a-z]{3})?-[A-Z]{2}",
        "primary_language": r"[a-z]{2,3}",
    }.items():
        bad = frame.loc[~frame[column].str.fullmatch(pattern), column].tolist()
        check(not bad, f"{column}: values outside {pattern}: {bad}")

    for column in ("iso2", "iso3", "iso_numeric", "name_pt", "name_en"):
        duplicated = frame.loc[frame[column].duplicated(), column].tolist()
        check(not duplicated, f"{column}: duplicated values {duplicated}")

    enums = {
        "writing_direction": {"ltr", "rtl"},
        "driving_side": {"left", "right"},
        "first_day_of_week": {"monday", "sunday", "saturday"},
        "time_format": {"12h", "24h"},
        "decimal_separator": {"comma", "period"},
        "grouping_separator": {"comma", "period", "space", "narrow_space", "apostrophe"},
        "paper_size": {"A4", "Letter"},
        "un_region": {"Africa", "Americas", "Asia", "Europe", "Oceania"},
        "continent_group": {"Africa", "America", "Asia", "Australia", "Caribbean", "Europe", "Melanesia", "Micronesia", "Oceania"},
    }
    for column, allowed in enums.items():
        bad = sorted(set(frame[column]) - allowed)
        check(not bad, f"{column}: unexpected values {bad}")

    for column in ("landlocked", "independent", "un_member", "has_rtl_official_language", "observes_dst"):
        bad = sorted(set(frame[column]) - {"True", "False"})
        check(not bad, f"{column}: not boolean {bad}")

    lat = frame["latitude"].astype(float)
    lon = frame["longitude"].astype(float)
    check(lat.between(-90, 90).all() and lon.between(-180, 180).all(), "coordinates out of range")

    # Borders: count matches the list and every border inside the dataset is symmetric.
    borders = {
        row.iso3: set(filter(None, row.borders_iso3.split("|"))) for row in frame.itertuples()
    }
    for row in frame.itertuples():
        check(int(row.border_count) == len(borders[row.iso3]), f"{row.iso3}: border_count differs from borders_iso3")
    for country, neighbours in borders.items():
        for other in neighbours:
            if other in borders:
                check(country in borders[other], f"border {country}-{other} is not symmetric")

    # Density is population / area within rounding.
    density = frame["population_millions"].astype(float) * 1e6 / frame["area_km2"].astype(float)
    off = frame.loc[(density - frame["density_per_km2"].astype(float)).abs() > density * 0.06 + 0.2, "iso3"]
    check(off.empty, f"density_per_km2 inconsistent for {off.tolist()}")

    # The writing direction must agree with the RTL flag.
    rtl_mismatch = frame.loc[(frame["writing_direction"] == "rtl") & (frame["has_rtl_official_language"] == "False"), "iso3"]
    check(rtl_mismatch.empty, f"rtl direction without RTL language: {rtl_mismatch.tolist()}")

    # The locale region must be the country itself.
    region = frame["locale"].str.extract(r"-([A-Z]{2})$")[0]
    check((region == frame["iso2"]).all(), "locale region differs from iso2")

    check(not frame.apply(lambda c: c.str.contains("‏| ", regex=True)).any().any(), "invisible characters left in data")
    check(not frame.apply(lambda c: c.str.match(r"^\s|.*\s$")).any().any(), "leading or trailing spaces left in data")

    # Brazilian Portuguese spelling: no European Portuguese forms left in the names.
    pt_pt = frame.loc[frame["name_pt"].str.contains(r"[éó]n|[éó]m|Vietname|Madagáscar|Holanda", regex=True), "name_pt"]
    check(pt_pt.empty, f"European Portuguese spellings in name_pt: {pt_pt.tolist()}")

    for message in failures:
        print("FAIL", message)
    print(f"{len(frame)} rows checked, {len(failures)} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
