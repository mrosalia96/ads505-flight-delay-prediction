"""Download BTS Reporting Carrier On-Time Performance monthly ZIPs for one year.

Source pattern (TranStats pre-zipped files):
  https://transtats.bts.gov/PREZIP/On_Time_Reporting_Carrier_On_Time_Performance_1987_present_{year}_{month}.zip

Raw ZIPs are written to data/raw/bts/. Large CSVs stay local (gitignored).
After download, filter to ORIGIN airports in a later notebook step.
"""

from __future__ import annotations

import argparse
import sys
import urllib.request
from pathlib import Path

BASE_URL = (
    "https://transtats.bts.gov/PREZIP/"
    "On_Time_Reporting_Carrier_On_Time_Performance_1987_present_{year}_{month}.zip"
)


def project_raw_bts_dir() -> Path:
    return Path(__file__).resolve().parents[1] / "data" / "raw" / "bts"


def download_month(year: int, month: int, out_dir: Path, overwrite: bool = False) -> Path:
    """Download one monthly ZIP. Returns the output path."""
    out_dir.mkdir(parents=True, exist_ok=True)
    filename = (
        f"On_Time_Reporting_Carrier_On_Time_Performance_1987_present_{year}_{month}.zip"
    )
    dest = out_dir / filename
    if dest.exists() and not overwrite:
        print(f"skip (exists): {dest.name}")
        return dest

    url = BASE_URL.format(year=year, month=month)
    print(f"downloading {url}")
    print(f"         -> {dest}")
    urllib.request.urlretrieve(url, dest)
    size_mb = dest.stat().st_size / (1024 * 1024)
    print(f"done: {dest.name} ({size_mb:.1f} MB)")
    return dest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--year", type=int, default=2023)
    parser.add_argument(
        "--months",
        type=int,
        nargs="+",
        default=list(range(1, 13)),
        help="Month numbers to download (default: 1-12)",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=None,
        help="Output directory (default: data/raw/bts)",
    )
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args(argv)

    out_dir = args.out_dir or project_raw_bts_dir()
    for month in args.months:
        if month < 1 or month > 12:
            print(f"invalid month: {month}", file=sys.stderr)
            return 1
        download_month(args.year, month, out_dir, overwrite=args.overwrite)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
