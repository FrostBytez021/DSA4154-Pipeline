# DSA4154-Pipeline
### Real-Time Ambient Air Quality Monitoring and Health Advisory System in Metro Manila
*University of Santo Tomas — College of Science, A.Y. 2025–2026*

---

## What?

This is an **automated data pipeline** that collects live air quality data across 17 monitoring stations in Metro Manila, stores it in a cloud database, and serves as the foundation for a public health advisory dashboard.

The pipeline tracks two key air pollutants — **PM10** and **PM2.5** (fine particulate matter) — and converts raw measurements into a standardized **Air Quality Index (AQI)** with human-readable health status labels (e.g., *"GOOD"*, *"FAIR"*, *"ACUTELY UNHEALTHY"*). This project addresses the lack of public awareness around air quality hazards in Metro Manila, where 13 million residents are exposed to unsafe pollution levels daily.

---

## Project Directory

```
DSA4154-Pipeline/
│
├── .github/
│   └── workflows/          # GitHub Actions automation (cron job scheduler)
│
├── extractor.py            # Main pipeline script — fetches, processes, and uploads data
├── requirements.txt        # Python dependencies needed to run the project
└── README.md               # You are here
```

### File Descriptions

| File | Description |
|------|-------------|
| `extractor.py` | The core script. Pulls live air quality data from the Open-Meteo API for 17 Metro Manila stations, computes AQI and health remarks, then appends the results to a Google Sheet. |
| `requirements.txt` | Lists all Python libraries the project depends on (`gspread`, `google-auth`, `requests`, `pandas`). Install these before running the script. |
| `.github/workflows/` | Contains the GitHub Actions YAML file that runs `extractor.py` automatically on a scheduled interval (cron job) — no manual triggering needed. |

> **Note:** A `credentials.json` file (Google Cloud Service Account key) is required to authenticate with Google Sheets. This file is **not committed to the repository** for security reasons. See setup instructions below.

---

## How

```
Open-Meteo API  →  extractor.py  →  Google Sheets (Cloud DB)  →  Dashboard (Tableau)
   (Live Data)      (Process &         (Data Storage)        (Visualization)
                     Upload)
```

1. **Data Extraction** — `extractor.py` queries the [Open-Meteo Air Quality API](https://air-quality-api.open-meteo.com/v1/air-quality) using the latitude/longitude coordinates of 17 monitoring stations across Metro Manila to retrieve current PM10 and PM2.5 values.

2. **Data Processing** — Raw JSON responses are parsed and structured into a `pandas` DataFrame. AQI values are mapped to health status categories using standard US AQI thresholds:

   | AQI Range | Health Status |
   |-----------|---------------|
   | 0 – 50 | 🟢 GOOD |
   | 51 – 100 | 🟡 FAIR |
   | 101 – 150 | 🟠 UNHEALTHY for Sensitive Groups |
   | 151 – 200 | 🔴 VERY UNHEALTHY |
   | 201 – 300 | 🟣 ACUTELY UNHEALTHY |
   | 301+ | ⚫ EMERGENCY |

3. **Data Storage** — Processed records are appended to a **Google Sheet** (`DSA4154_Dummy_DB`) acting as a live cloud database, authenticated securely via a Google Cloud Service Account.

4. **Automation** — The script is scheduled to run at regular intervals using **GitHub Actions** (cron job), ensuring the database stays continuously updated without manual intervention.

5. **Visualization** — The Google Sheet feeds into a connected **Tableau dashboard** that displays KPI cards, time-series trend charts, station ranking bar charts, and a geographic map of Metro Manila with color-coded pollution severity.

---

## Monitoring Stations Covered

The pipeline collects data from 17 stations across Metro Manila:

| Station | City |
|---------|------|
| Caloocan (Univ. of East) | Caloocan |
| Las Pinas City | Las Piñas |
| Makati | Makati |
| Malabon City | Malabon |
| Mandaluyong | Mandaluyong |
| Manila City Hall | Manila |
| Marikina CEMO | Marikina |
| Muntinlupa (Filinvest City) | Muntinlupa |
| Navotas | Navotas |
| Paranaque City | Parañaque |
| Pasay | Pasay |
| Pasig City | Pasig |
| Quezon City (Ateneo) | Quezon City |
| Quezon City (SMPH Commonwealth) | Quezon City |
| San Juan City | San Juan |
| Taguig (TUP) | Taguig |
| Valenzuela | Valenzuela |

---

## Setup

### Prerequisites
- Python 3.8 or higher
- A Google Cloud Service Account with access to the target Google Sheet
- Git

### 1. Clone the repository
```bash
git clone https://github.com/FrostBytez021/DSA4154-Pipeline.git
cd DSA4154-Pipeline
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your credentials
Place your Google Cloud Service Account key file in the root directory and name it `credentials.json`. This file is used by the script to authenticate with Google Sheets.

> ⚠️ **Never commit `credentials.json` to GitHub.** Add it to `.gitignore` to keep it private.

For automated runs via GitHub Actions, store the credentials as a **GitHub Secret** named `GCP_CREDENTIALS` (the script already supports this).

### 4. Run the script manually
```bash
python extractor.py
```

The script will print a live table of extracted air quality data in the terminal, then upload the records to Google Sheets.

---

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `requests` | Fetches data from the Open-Meteo API |
| `pandas` | Structures and formats the extracted data |
| `gspread` | Interfaces with Google Sheets |
| `google-auth` | Handles Google Cloud authentication |

Install all at once:
```bash
pip install -r requirements.txt
```

---

## Authors

Mikaela Angela C. Carlos, Drei Cerise B. Dayag, Althea Marie S. Habaluyas, Marga Lonyle N. Lominoque, Maria Camela M. Oliva, and Jeanne Margarette Vitor

*Department of Mathematics and Physics, College of Science, University of Santo Tomas*

---

## Data Source

Air quality data is sourced from the **[Open-Meteo Air Quality API](https://air-quality-api.open-meteo.com/v1/air-quality)** — a free, open-source API that provides real-time environmental data without authentication or unauthorized scraping of government dashboards.
