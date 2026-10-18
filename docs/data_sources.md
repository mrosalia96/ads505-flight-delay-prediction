# Data sources and acquisition

This document tells a colleague how to obtain the same raw inputs used in the analysis. Raw files live under `data/raw/` and are excluded from Git because of size.

## Analysis sample (locked for v1)

- **Year:** 2023 (January–December)
- **Origin airports:** SAN, LAX, PHX, DEN, SEA
- **Unit of analysis:** One scheduled flight departure (BTS on-time performance row)
- **Primary outcome:** Departure delay indicator — late if `DEP_DELAY >= 15` minutes (BTS standard threshold), else on-time
- **Weather join key (planned):** Origin airport → nearby NCEI station; flight date (and hour if hourly weather is used)

## Source 1 — BTS Airline On-Time Performance

**Name:** Airline On-Time Performance Data  
**Publisher:** U.S. Department of Transportation, Bureau of Transportation Statistics (BTS)  
**Access:** https://www.transtats.bts.gov/  
**Direct product path (TranStats):** Aviation → Airline On-Time Performance Data  
**Local path:** `data/raw/bts/`

### What to download

TranStats publishes **pre-zipped monthly** Reporting Carrier On-Time files:

```text
https://transtats.bts.gov/PREZIP/On_Time_Reporting_Carrier_On_Time_Performance_1987_present_{year}_{month}.zip
```

Example (January 2023):

```text
https://transtats.bts.gov/PREZIP/On_Time_Reporting_Carrier_On_Time_Performance_1987_present_2023_1.zip
```

Each ZIP contains a full-national monthly CSV (~110 columns). Confirmed useful fields in the 2023 files include: `Year`, `Month`, `FlightDate`, `Origin`, `Dest`, `CRSDepTime`, `DepTime`, `DepDelay`, `DepDel15` (BTS 15-minute departure-delay flag), `Distance`, `DayOfWeek`, `Cancelled`, and reporting-airline identifiers. After download, filter in Python to **`Origin`** in `{SAN, LAX, PHX, DEN, SEA}`. Do **not** use delay-cause fields (`CarrierDelay`, `WeatherDelay`, etc.) as predictive features (leakage).

### Download helper

From the repo root (requires network):

```bash
# smoke-test one month
python src/download_bts.py --year 2023 --months 1

# full year
python src/download_bts.py --year 2023
```

Files land in `data/raw/bts/` (gitignored except folder placeholders).

### Suggested file naming (as published by BTS)

```text
data/raw/bts/On_Time_Reporting_Carrier_On_Time_Performance_1987_present_2023_1.zip
...
data/raw/bts/On_Time_Reporting_Carrier_On_Time_Performance_1987_present_2023_12.zip
```

### APA 7 dataset reference (draft)

U.S. Department of Transportation, Bureau of Transportation Statistics. (n.d.). *Airline on-time performance data* [Data set]. https://www.transtats.bts.gov/

*(Confirm retrieval year/month in the final brief and notebook once downloads are complete.)*

## Source 2 — NOAA / NCEI weather observations

**Name:** Local Climatological Data / station observations (NCEI)  
**Publisher:** National Oceanic and Atmospheric Administration, National Centers for Environmental Information (NCEI)  
**Access:** https://www.ncei.noaa.gov/  
**Local path:** `data/raw/noaa/`

### Planned stations (near origin airports)

| Airport | Approx. area | Notes |
|---------|--------------|--------|
| SAN | San Diego, CA | Prefer station closest to SAN with continuous 2023 coverage |
| LAX | Los Angeles, CA | Same |
| PHX | Phoenix, AZ | Same |
| DEN | Denver, CO | Same |
| SEA | Seattle, WA | Same |

Variables of interest: temperature, wind speed, precipitation / weather indicators aligned to departure date (and hour if using hourly LCD).

Exact station IDs will be recorded here after download, for example:

```text
data/raw/noaa/<station_id>_2023.csv
```

### APA 7 dataset reference (draft)

National Oceanic and Atmospheric Administration, National Centers for Environmental Information. (n.d.). *Local climatological data* [Data set]. https://www.ncei.noaa.gov/

## Processed flight sample (built locally)

After downloading all 12 monthly ZIPs for 2023:

```bash
python src/build_flights_sample.py --year 2023
```

Writes `data/processed/flights_origins_2023.parquet` (gitignored).  
**Retrieval / build note:** BTS ZIPs downloaded 2026-10-18; filtered sample has **914,796** rows for origins SAN, LAX, PHX, DEN, SEA.

## Reproducibility checklist

1. Create `data/raw/bts/` and `data/raw/noaa/` if they do not exist.
2. Download 2023 monthly BTS files (`python src/download_bts.py --year 2023`).
3. Build the filtered sample (`python src/build_flights_sample.py --year 2023`).
4. Download 2023 NOAA extracts for stations serving those airports (next step).
5. Continue analysis in `notebooks/technical_notebook.ipynb` (built section by section; re-run from a clean kernel).

## Notes on leakage

Delay-*cause* fields and post-departure actuals must not be used as predictive features for a pre-departure decision. Weather known at or before scheduled departure is in scope; information that exists only after the delay occurs is out of scope for the model features.
