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

## Source 2 — NOAA ASOS hourly weather (via IEM)

**Name:** Automated Surface Observing System (ASOS) METARs  
**Publisher:** National Oceanic and Atmospheric Administration (NOAA) ASOS network  
**Access path used:** Iowa Environmental Mesonet (IEM) ASOS request service (public redistribution of NOAA ASOS)  
https://mesonet.agron.iastate.edu/request/download.phtml  
**Local path:** `data/raw/noaa/`

### Stations (airport ASOS ids, local timezone for hour alignment)

| Origin | ASOS station | Timezone |
|--------|--------------|----------|
| SAN | SAN | America/Los_Angeles |
| LAX | LAX | America/Los_Angeles |
| PHX | PHX | America/Phoenix |
| DEN | DEN | America/Denver |
| SEA | SEA | America/Los_Angeles |

**Variables pulled:** `tmpf` (temp °F), `dwpf` (dewpoint °F), `sknt` (wind speed knots), `p01i` (hourly precip inches), `vsby` (visibility miles).

### Download / build

```bash
python src/download_weather.py --year 2023
python src/build_weather_hourly.py --year 2023
# → data/processed/weather_hourly_2023.parquet
```

Raw files look like `data/raw/noaa/asos_SAN_2023.csv`.  
**Retrieval note:** downloaded 2026-10-18; hourly aggregate has **43,661** rows.

Join key to flights: `(Origin, FlightDate, crs_dep_hour)` ↔ `(Origin, weather_date, weather_hour)`.

### APA 7 dataset reference (draft)

Iowa Environmental Mesonet. (n.d.). *ASOS network data* [Data set]. Iowa State University. https://mesonet.agron.iastate.edu/  
(Underlying observations: NOAA Automated Surface Observing System.)

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
4. Download ASOS weather and build hourly table (`download_weather.py`, `build_weather_hourly.py`).
5. Continue analysis in `notebooks/technical_notebook.ipynb` (built section by section; re-run from a clean kernel).

## Notes on leakage

Delay-*cause* fields and post-departure actuals must not be used as predictive features for a pre-departure decision. Weather known at or before scheduled departure is in scope; information that exists only after the delay occurs is out of scope for the model features.
