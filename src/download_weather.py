"""Download NOAA ASOS hourly weather via Iowa Environmental Mesonet (IEM).

IEM redistributes ASOS METARs from the NOAA network. Fixed URL pattern makes
the pull reproducible without a GUI.

Example:
  python src/download_weather.py --year 2023
"""

from __future__ import annotations

import argparse
import urllib.parse
import urllib.request
from pathlib import Path

# BTS Origin code -> (ASOS station id, IANA timezone for local clock alignment)
AIRPORTS = {
    "SAN": ("SAN", "America/Los_Angeles"),
    "LAX": ("LAX", "America/Los_Angeles"),
    "PHX": ("PHX", "America/Phoenix"),
    "DEN": ("DEN", "America/Denver"),
    "SEA": ("SEA", "America/Los_Angeles"),
}

VARS = ("tmpf", "dwpf", "sknt", "p01i", "vsby")


def project_noaa_dir() -> Path:
    return Path(__file__).resolve().parents[1] / "data" / "raw" / "noaa"


def asos_url(station: str, tz: str, year: int) -> str:
    params = [
        ("station", station),
        *[("data", v) for v in VARS],
        ("year1", str(year)),
        ("month1", "1"),
        ("day1", "1"),
        ("year2", str(year)),
        ("month2", "12"),
        ("day2", "31"),
        ("tz", tz),
        ("format", "onlycomma"),
        ("latlon", "no"),
        ("elev", "no"),
        ("missing", "null"),
        ("trace", "0.0001"),
        ("direct", "yes"),
        ("report_type", "3"),
    ]
    return "https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?" + urllib.parse.urlencode(
        params
    )


def download_airport(origin: str, year: int, out_dir: Path, overwrite: bool = False) -> Path:
    station, tz = AIRPORTS[origin]
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / f"asos_{origin}_{year}.csv"
    if dest.exists() and not overwrite:
        print(f"skip (exists): {dest.name}")
        return dest

    url = asos_url(station, tz, year)
    print(f"downloading {origin} ({station}, {tz})")
    print(f"  {url}")
    urllib.request.urlretrieve(url, dest)
    size_kb = dest.stat().st_size / 1024
    print(f"done: {dest.name} ({size_kb:.0f} KB)")
    return dest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--year", type=int, default=2023)
    parser.add_argument(
        "--airports",
        nargs="+",
        default=list(AIRPORTS.keys()),
        choices=list(AIRPORTS.keys()),
    )
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    out_dir = project_noaa_dir()
    for origin in args.airports:
        download_airport(origin, args.year, out_dir, overwrite=args.overwrite)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
