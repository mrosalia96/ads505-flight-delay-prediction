# ADS 505 — Flight Departure Delay Prediction

**Team:** 4 (individual project, instructor-approved)  
**Author:** Michael Rosalia  
**Repository:** https://github.com/mrosalia96/ads505-flight-delay-prediction

## Purpose

Predict which U.S. flights are likely to depart late using historical Bureau of Transportation Statistics (BTS) on-time performance data joined with NOAA weather observations. The goal is to give airline and airport decision-makers an earlier view of delay risk so they can prioritize staffing, gate planning, and passenger communication.

This repository supports the course technical notebook, business brief, and executive presentation. Analysis should be reproducible from a clean clone with minimal setup.

## Project scope (v1 sample)

To keep the project runnable in a day while remaining realistic:

| Dimension | Choice |
|-----------|--------|
| Target | Binary departure delay (≥ 15 minutes late vs on-time), consistent with BTS reporting |
| Year | Calendar year **2023** |
| Airports (origin) | **SAN, LAX, PHX, DEN, SEA** |
| Flight data | BTS Airline On-Time Performance (monthly files) |
| Weather | NOAA / NCEI daily or hourly station observations near each airport |
| Holdout | Train / validation / test split by time (no leakage from future flights) |

Rationale: San Diego–centric regional sample with a few major hubs, one full year for seasonality, and a manageable row count (hundreds of thousands of flights rather than the full national archive).

Details and APA-style source citations: [`docs/data_sources.md`](docs/data_sources.md)  
Analysis boundaries and decision framing: [`docs/project_scope.md`](docs/project_scope.md)

## Repository layout

```text
ads505-flight-delay-prediction/
├── data/
│   ├── raw/          # downloaded source files (not committed; see .gitignore)
│   └── processed/    # cleaned analysis tables (not committed)
├── docs/             # data sources, scope, notes for collaborators
├── notebooks/        # Jupyter analysis notebooks (.ipynb)
├── reports/          # exported figures or brief supporting tables (optional)
├── src/              # reusable Python helpers (if needed)
├── requirements.txt
└── README.md
```

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/mrosalia96/ads505-flight-delay-prediction.git
   cd ads505-flight-delay-prediction
   ```

2. Create and activate the project conda env (recommended):

   ```bash
   conda create -n ads505 python=3.11 -y
   conda activate ads505
   pip install -r requirements.txt ipykernel
   python -m ipykernel install --user --name ads505 --display-name "Python (ads505)"
   ```

   In Jupyter / Cursor, select kernel **Python (ads505)**.

3. Or use a venv instead:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. Obtain raw data (files are large and are **not** stored in Git):

   - Follow the download steps in [`docs/data_sources.md`](docs/data_sources.md).
   - Place BTS CSVs under `data/raw/bts/`.
   - Place NOAA extracts under `data/raw/noaa/`.

## How to run

1. Confirm raw data paths match those described in `docs/data_sources.md`.
2. Open Jupyter from the repo root:

   ```bash
   jupyter notebook notebooks/
   ```

3. Open the technical notebook and run cells top to bottom as sections are added:

   - [`notebooks/technical_notebook.ipynb`](notebooks/technical_notebook.ipynb)

4. Download BTS monthly ZIPs, then build the filtered origin sample:

   ```bash
   python src/download_bts.py --year 2023 --months 1   # smoke test
   python src/download_bts.py --year 2023              # full year
   python src/build_flights_sample.py --year 2023      # → data/processed/
   python src/download_weather.py --year 2023          # NOAA ASOS via IEM
   python src/build_weather_hourly.py --year 2023
   ```

Re-run from a fresh kernel when validating reproducibility.

## Member contributions

| Member | Contributions |
|--------|----------------|
| Michael Rosalia | All project work: data acquisition and documentation, EDA, preprocessing, modeling, evaluation, technical notebook, business brief, executive slides/video, and repository maintenance |

## Course deliverables (naming)

| Deliverable | Expected file name |
|-------------|-------------------|
| Technical notebook (PDF export) | `Technical_Notebook-Team4.pdf` |
| Business brief | `Business-Brief_Team4.pdf` |
| Executive slides | `Executive-Slides-Team4.pptx` |
| Executive video | `Executive-Video-Team4.mp4` |

Include this repository URL in the technical notebook and business brief. Adjust GitHub visibility so the instructor can view the commit history.

## License / data use

Flight and weather inputs are public U.S. government data. Cite sources as documented in `docs/data_sources.md`. This coursework repository is for educational use.
