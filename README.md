# Flight Departure Delay Prediction

Predict whether a U.S. flight will depart 15+ minutes late using Bureau of Transportation Statistics (BTS) on-time data and NOAA ASOS weather at the origin. Built for a same-day watch list before busy departure windows (staffing, buffers, passenger messaging).

**Author:** Michael Rosalia  
**Repo:** https://github.com/mrosalia96/ads505-flight-delay-prediction

## Scope

- **Year:** 2023  
- **Origin airports:** SAN, LAX, PHX, DEN, SEA  
- **Target:** `DepDel15` (BTS 15-minute departure delay flag)  
- **Split:** chronological train (Jan–Aug) / validation (Sep–Oct) / test (Nov–Dec)

Data documentation and APA-style citations: [`docs/data_sources.md`](docs/data_sources.md)

## Setup

```bash
git clone https://github.com/mrosalia96/ads505-flight-delay-prediction.git
cd ads505-flight-delay-prediction

conda create -n ads505 python=3.11 -y
conda activate ads505
pip install -r requirements.txt ipykernel
python -m ipykernel install --user --name ads505 --display-name "Python (ads505)"
```

Select kernel **Python (ads505)** in Jupyter or Cursor.

## Reproduce the analysis

Raw files are not in Git (size). Download and build locally, then run the notebook:

```bash
python src/download_bts.py --year 2023
python src/build_flights_sample.py --year 2023
python src/download_weather.py --year 2023
python src/build_weather_hourly.py --year 2023

jupyter notebook notebooks/technical_notebook.ipynb
```

Run all cells top to bottom from a clean kernel.

## Layout

```text
data/raw/          # BTS ZIPs and ASOS CSVs (gitignored)
data/processed/    # filtered flights + hourly weather (gitignored)
docs/              # data sources and project notes
notebooks/         # technical_notebook.ipynb
src/               # download and build helpers
requirements.txt
```

Course deliverables (business brief, executive slides, PDFs) live in the local ADS505 course folder only, not in this GitHub repository.

## Contributions

| Member | Work |
|--------|------|
| Michael Rosalia | Data acquisition, EDA, modeling, technical notebook, business deliverables, repository |
