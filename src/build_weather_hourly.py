"""Aggregate raw ASOS CSVs to hourly weather by origin airport.

Writes data/processed/weather_hourly_{year}.parquet for joining to flights on
(Origin, FlightDate, crs_dep_hour).
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

ORIGINS = ("SAN", "LAX", "PHX", "DEN", "SEA")


def project_paths() -> tuple[Path, Path]:
    root = Path(__file__).resolve().parents[1]
    return root / "data" / "raw" / "noaa", root / "data" / "processed"


def load_airport_hourly(csv_path: Path, origin: str) -> pd.DataFrame:
    frame = pd.read_csv(csv_path, na_values=["null", "M", ""])
    if frame.empty:
        raise ValueError(f"Empty weather file: {csv_path.name}")

    frame["valid"] = pd.to_datetime(frame["valid"])
    frame["weather_date"] = frame["valid"].dt.floor("D")
    frame["weather_hour"] = frame["valid"].dt.hour

    for col in ("tmpf", "dwpf", "sknt", "p01i", "vsby"):
        if col in frame.columns:
            frame[col] = pd.to_numeric(frame[col], errors="coerce")

    hourly = (
        frame.groupby(["weather_date", "weather_hour"], as_index=False)
        .agg(
            tmpf=("tmpf", "mean"),
            dwpf=("dwpf", "mean"),
            sknt=("sknt", "mean"),
            p01i=("p01i", "sum"),
            vsby=("vsby", "mean"),
            n_obs=("tmpf", "size"),
        )
    )
    hourly["Origin"] = origin
    return hourly


def build_weather(year: int) -> Path:
    raw_dir, processed_dir = project_paths()
    processed_dir.mkdir(parents=True, exist_ok=True)

    pieces: list[pd.DataFrame] = []
    for origin in ORIGINS:
        path = raw_dir / f"asos_{origin}_{year}.csv"
        if not path.exists():
            raise FileNotFoundError(
                f"Missing {path}. Run: python src/download_weather.py --year {year}"
            )
        print(f"aggregating {path.name} ...")
        pieces.append(load_airport_hourly(path, origin))

    weather = pd.concat(pieces, ignore_index=True)
    out = processed_dir / f"weather_hourly_{year}.parquet"
    weather.to_parquet(out, index=False)
    print(f"wrote {out} ({len(weather):,} hourly rows)")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--year", type=int, default=2023)
    args = parser.parse_args()
    build_weather(args.year)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
