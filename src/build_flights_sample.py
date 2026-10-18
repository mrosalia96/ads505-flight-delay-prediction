"""Filter downloaded BTS monthly ZIPs to the project airport sample.

Reads ZIPs from data/raw/bts/, keeps Origin in the configured airport set,
selects modeling/EDA columns, and writes a single parquet (preferred) or CSV
to data/processed/.
"""

from __future__ import annotations

import argparse
import zipfile
from pathlib import Path

import pandas as pd

ORIGIN_AIRPORTS = ("SAN", "LAX", "PHX", "DEN", "SEA")
ANALYSIS_YEAR = 2023

# Keep lean; expand later if EDA needs more fields.
KEEP_COLUMNS = [
    "Year",
    "Month",
    "DayofMonth",
    "DayOfWeek",
    "FlightDate",
    "Reporting_Airline",
    "Flight_Number_Reporting_Airline",
    "Origin",
    "OriginCityName",
    "Dest",
    "DestCityName",
    "CRSDepTime",
    "DepTime",
    "DepDelay",
    "DepDelayMinutes",
    "DepDel15",
    "DepTimeBlk",
    "Cancelled",
    "Diverted",
    "CRSElapsedTime",
    "Distance",
]


def project_paths() -> tuple[Path, Path]:
    root = Path(__file__).resolve().parents[1]
    return root / "data" / "raw" / "bts", root / "data" / "processed"


def list_month_zips(bts_dir: Path, year: int) -> list[Path]:
    pattern = f"On_Time_Reporting_Carrier_On_Time_Performance_1987_present_{year}_*.zip"
    zips = sorted(bts_dir.glob(pattern), key=lambda p: int(p.stem.rsplit("_", 1)[-1]))
    return zips


def load_filtered_month(zip_path: Path, origins: tuple[str, ...]) -> pd.DataFrame:
    with zipfile.ZipFile(zip_path) as zf:
        csv_names = [n for n in zf.namelist() if n.lower().endswith(".csv")]
        if not csv_names:
            raise FileNotFoundError(f"No CSV inside {zip_path.name}")
        with zf.open(csv_names[0]) as handle:
            # Read only needed columns when present.
            header = pd.read_csv(handle, nrows=0)
            usecols = [c for c in KEEP_COLUMNS if c in header.columns]
            handle.seek(0)
            frame = pd.read_csv(handle, usecols=usecols, low_memory=False)

    if "Origin" not in frame.columns:
        raise KeyError(f"Origin column missing in {zip_path.name}")

    frame = frame[frame["Origin"].isin(origins)].copy()
    frame["source_zip"] = zip_path.name
    return frame


def build_sample(
    year: int = ANALYSIS_YEAR,
    origins: tuple[str, ...] = ORIGIN_AIRPORTS,
    bts_dir: Path | None = None,
    out_dir: Path | None = None,
) -> Path:
    raw_bts, processed = project_paths()
    bts_dir = bts_dir or raw_bts
    out_dir = out_dir or processed
    out_dir.mkdir(parents=True, exist_ok=True)

    zips = list_month_zips(bts_dir, year)
    if not zips:
        raise FileNotFoundError(
            f"No BTS ZIPs for {year} in {bts_dir}. Run src/download_bts.py first."
        )

    pieces: list[pd.DataFrame] = []
    for zip_path in zips:
        print(f"filtering {zip_path.name} ...")
        piece = load_filtered_month(zip_path, origins)
        print(f"  kept {len(piece):,} rows")
        pieces.append(piece)

    flights = pd.concat(pieces, ignore_index=True)
    flights["FlightDate"] = pd.to_datetime(flights["FlightDate"], errors="coerce")

    # Avoid Arrow extension-dtype edge cases across pandas/pyarrow versions
    for col in flights.select_dtypes(include=["object"]).columns:
        flights[col] = flights[col].astype("string").astype(object)

    out_parquet = out_dir / f"flights_origins_{year}.parquet"
    out_csv = out_dir / f"flights_origins_{year}.csv"

    try:
        flights.to_parquet(out_parquet, index=False, engine="pyarrow")
        out_path = out_parquet
    except Exception as exc:  # noqa: BLE001 - fall back for any parquet engine issue
        print(f"parquet write failed ({type(exc).__name__}: {exc}); writing CSV instead")
        flights.to_csv(out_csv, index=False)
        out_path = out_csv

    print(
        f"wrote {out_path} ({len(flights):,} rows, "
        f"origins={sorted(flights['Origin'].unique())})"
    )
    return out_path


def default_sample_path(year: int = ANALYSIS_YEAR, out_dir: Path | None = None) -> Path | None:
    """Return existing processed sample path (parquet preferred), else None."""
    _, processed = project_paths()
    out_dir = out_dir or processed
    parquet = out_dir / f"flights_origins_{year}.parquet"
    csv = out_dir / f"flights_origins_{year}.csv"
    if parquet.exists():
        return parquet
    if csv.exists():
        return csv
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--year", type=int, default=ANALYSIS_YEAR)
    args = parser.parse_args()
    build_sample(year=args.year)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
