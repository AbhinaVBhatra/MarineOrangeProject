# Dataset Documentation & Provenance Report

**Project Title:** Marine Condition Analysis and Classification Using Data Mining  
**Document:** Dataset Provenance, Schema, Missingness Analysis, and Preprocessing Specification  
**Location:** `./ResearchPaper/Dataset_Documentation.md`  
**Date:** October 2026  
**Curriculum Context:** B.Tech Computer Science Engineering — Data Mining  

---

## 1. Dataset Overview and Provenance

- **Dataset Title:** National Data Buoy Center (NDBC) Standard Meteorological Buoy Data, 1970–present
- **Dataset Identifier (ERDDAP ID):** `cwwcNDBCMet`
- **Data Provider:** National Oceanic and Atmospheric Administration (NOAA) CoastWatch / National Marine Fisheries Service (NMFS) Southwest Fisheries Science Center (SWFSC) Environmental Research Division (ERD), in collaboration with the NOAA National Data Buoy Center (NDBC).
- **Access Protocol & Endpoint:** NOAA CoastWatch ERDDAP Server (`tabledap` endpoint):  
  [https://coastwatch.pfeg.noaa.gov/erddap/tabledap/cwwcNDBCMet.html](https://coastwatch.pfeg.noaa.gov/erddap/tabledap/cwwcNDBCMet.html)
- **Original Downloaded File:** `Downloads/cwwcNDBCMet_98c8_d2df_4d0a.csv`
- **Working Archive Location:** `./data/raw.csv` (154,625 bytes, byte-for-byte exact copy of original download; original remains unedited).
- **Date Accessed:** October 2026
- **License and Terms of Use:** Public Domain (U.S. Government work). Free and unrestricted scientific reuse. Explicit disclaimer: *"These data are not intended for legal, navigation, or operational safety use; they may contain uncalibrated sensor inaccuracies."*
- **Geographic Attribution Notice:** All observations originate **exclusively from United States coastal and offshore territorial waters** (Northwest Atlantic Ocean and northern Gulf of Mexico). **The dataset contains zero observations from Indian territorial waters (Arabian Sea, Bay of Bengal, or Indian Ocean).**

---

## 2. Temporal and Geographic Coverage

### 2.1 Temporal Bounds
- **Temporal Query Range:** 2025-01-01 00:00:00Z to 2025-06-30 23:50:00Z (First half of calendar year 2025 = 181 calendar days).
- **Sampling Interval:** 3-hourly nominal telemetry cadence (8 nominal observations per 24-hour cycle: 00:00, 03:00, 06:00, 09:00, 12:00, 15:00, 18:00, 21:00 UTC).

### 2.2 Geographic Stations
The observational data contains records from two distinct moored marine observation stations operated under the NOAA NDBC network:

| Station ID | Station Name / Platform Type | Latitude | Longitude | Water Depth / Elev. | Geographic Basin | Reporting Span in Dataset |
|:---:|:---|:---:|:---:|:---:|:---|:---:|
| **42040** | Luke Offshore Test Platform (C-MAN / Fixed Platform) | 29.212° N | -88.207° E (-88.207° W) | 207 m (Mississippi Canyon) | Northern Gulf of Mexico | 2025-01-01 00:00:00Z to 2025-06-30 23:50:00Z (181.0 days) |
| **41002** | South Hatteras Moored Ocean Buoy (3-meter discus buoy) | 31.887° N | -74.921° E (-74.921° W) | 3,749 m (Deep Atlantic) | Northwest Atlantic Ocean | 2025-04-27 09:00:00Z to 2025-06-30 23:50:00Z (64.6 days) |

---

## 3. Forensic Analysis: The 1,967 vs. ~4,300 Row Gap

### 3.1 Theoretical Expectation vs. Observational Reality
In preliminary research design, an aggregate sample of approximately ~4,300 rows was anticipated. The theoretical calculation was derived as follows:
$$\text{Expected Days} = 181 \text{ days (Jan 1 to Jun 30, 2025)}$$
$$\text{Readings per Day} = \frac{24\text{ hours}}{3\text{ hours}} = 8\text{ nominal observations}$$
$$\text{Nominal Slots per Buoy} = 181 \times 8 = 1,448\text{ timestamps}$$
$$\text{Nominal Total for 3 Buoys} = 1,448 \times 3 = 4,344\text{ records}$$

Upon ingest into the Python data environment and Orange Data Mining, the raw table loaded with exactly **1,967 rows**—an apparent deficit of **2,377 rows**.

### 3.2 Quantitative Attribution of the Deficit
Forensic auditing of `data/raw.csv` reveals two distinct empirical causes:
1. **Omission of the 3rd Target Station ($N = 0$ rows, deficit of -1,448 rows):** The download query captured only two buoy stations (42040 and 41002). A planned third station was absent from the returned ERDDAP payload.
2. **Delayed Deployment / Telemetry Outage at Station 41002 ($N = 518$ rows, deficit of -930 rows):** While Station 42040 operated continuously across all 181 days ($N = 1,449$ records, matching theoretical expectations), Station 41002 only began streaming telemetry on April 27, 2025 at 09:00:00 UTC. Over 116 calendar days (~930 expected 3-hourly intervals) from January 1 through April 27 were unrecorded.

$$\text{Observed Rows} = 1,449\text{ (Station 42040)} + 518\text{ (Station 41002)} = 1,967\text{ records}$$

In strict conformance with scientific integrity, no synthetic data was fabricated to fill this temporal gap.

---

## 4. Attribute Schema and Variable Definitions

The raw dataset contains 12 attributes formatted in standard NOAA NDBC ERDDAP naming conventions (`name (unit)`):

| Attribute Name | Variable Type | Storage Type | Physical Units | Physical Definition & Sensor Method |
|:---|:---:|:---:|:---:|:---|
| `station` | Identifier | Integer | Dimensionless | 5-character WMO / NDBC station identification code. |
| `time (UTC)` | Temporal | String (ISO 8601) | UTC timestamp | Coordinated Universal Time of observation (`YYYY-MM-DDTHH:MM:SSZ`). |
| `latitude (degrees_north)` | Spatial | Float64 | Degrees North | Geographic latitude of buoy mooring. |
| `longitude (degrees_east)` | Spatial | Float64 | Degrees East | Geographic longitude of buoy mooring (values <0 indicate West). |
| `WSPD (m s-1)` | Continuous | Float64 | $\text{m}\cdot\text{s}^{-1}$ | Sustained wind speed averaged over an eight-minute sampling period. |
| `GST (m s-1)` | Continuous | Float64 | $\text{m}\cdot\text{s}^{-1}$ | Peak wind gust speed recorded during the ten-minute observation window. |
| `WVHT (m)` | Continuous | Float64 | Meters ($\text{m}$) | Significant wave height: average height of highest one-third of waves. |
| `DPD (s)` | Continuous | Float64 | Seconds ($\text{s}$) | Dominant wave period: period corresponding to the spectral peak frequency. |
| `APD (s)` | Continuous | Float64 | Seconds ($\text{s}$) | Average wave period: average period of all waves during the spectral record. |
| `BAR (hPa)` | Continuous | Float64 | Hectopascals ($\text{hPa}$) | Sea-level barometric atmospheric pressure. |
| `ATMP (degree_C)` | Continuous | Float64 | Degrees Celsius (°C) | Air temperature recorded at anemometer/sensor mast height. |
| `WTMP (degree_C)` | Continuous | Float64 | Degrees Celsius (°C) | Sea surface water temperature recorded by hull-mounted thermistor. |

---

## 5. Quantitative Missingness Audit

### 5.1 Reconciling Orange's "34% Missing Values" Diagnostic
When `raw.csv` is loaded into Orange Data Mining, the summary statistics window displays **"34% missing values"**. This was audited and mathematically reconciled:
- In Orange's domain architecture, the 11 numeric attributes are ingested into the feature matrix $X$, while `time (UTC)` is cataloged as a meta-variable.
- Total numeric cells in feature matrix:
  $$\text{Total Feature Cells} = 1,967\text{ rows} \times 11\text{ features} = 21,637\text{ cells}$$
- Total missing (NaN) values across the 11 features: exactly **7,358 cells**.
- The exact missingness percentage is:
  $$\text{Orange Missing Rate} = \frac{7,358}{21,637} \times 100 = 34.0066\% \approx 34.01\%$$

### 5.2 Attribute-by-Attribute Missingness Distribution

| Attribute | Total Records | Valid Count | Missing Count | Missing Percentage | Sensor Status / Operational Root Cause |
|:---|:---:|:---:|:---:|:---:|:---|
| `station` | 1,967 | 1,967 | 0 | 0.00% | Identifier metadata; 100% complete. |
| `time (UTC)` | 1,967 | 1,967 | 0 | 0.00% | Temporal metadata; 100% complete. |
| `latitude` | 1,967 | 1,967 | 0 | 0.00% | Static mooring position; 100% complete. |
| `longitude` | 1,967 | 1,967 | 0 | 0.00% | Static mooring position; 100% complete. |
| `WSPD (m s-1)` | 1,967 | 1,965 | 2 | 0.10% | Wind sensor; 2 missing readouts at Station 42040. |
| `GST (m s-1)` | 1,967 | 1,965 | 2 | 0.10% | Gust sensor; 2 missing readouts at Station 42040. |
| `WVHT (m)` | 1,967 | 0 | **1,967** | **100.00%** | Accelerometer payload unequipped or unrecorded on both buoys. |
| `DPD (s)` | 1,967 | 0 | **1,967** | **100.00%** | Wave spectral payload unequipped or unrecorded on both buoys. |
| `APD (s)` | 1,967 | 0 | **1,967** | **100.00%** | Wave spectral payload unequipped or unrecorded on both buoys. |
| `BAR (hPa)` | 1,967 | 1,965 | 2 | 0.10% | Barometer; 2 missing readouts at Station 42040. |
| `ATMP (degree_C)` | 1,967 | 1,965 | 2 | 0.10% | Air thermometer; 2 missing readouts at Station 42040. |
| `WTMP (degree_C)` | 1,967 | 518 | **1,449** | **73.67%** | Station 42040 lacks water thermistor (0/1,449); Station 41002 has 518/518. |

---

## 6. Preprocessing Methodology and Cleaning Rules

### 6.1 Missingness Thresholding (>50.0% Rule)
- **Rule Formulation:** Attributes exhibiting missingness exceeding 50.0% of observational instances must be eliminated from core multivariate analysis.
- **Enforcement:** `WVHT (m)`, `DPD (s)`, and `APD (s)` exhibit **100.00% missingness** (zero observations). They provide zero variance and are purged entirely.

### 6.2 The Water Temperature (WTMP) Geographic Trade-Off
- `WTMP (degree_C)` exhibits 73.67% missingness globally, but this missingness is structurally localized:
  - Station 42040 (Gulf of Mexico): 100% missing (no water temperature sensor installed).
  - Station 41002 (Atlantic): 100% present ($N = 518$ valid readings).
- **Trade-Off Analysis:** Mandating `WTMP` in the primary dataset forces listwise deletion of all 1,449 records of Station 42040. This would destroy spatial diversity, discarding 73.7% of the total dataset and turning the analysis into an isolated single-buoy study.
- **Architectural Resolution:**
  1. **Primary Cleaned Core Dataset (`cleaned_core.csv`):** Retains `WSPD`, `GST`, `BAR`, and `ATMP` across both stations. Filters out 4 intermittent sensor dropouts. **$N = 1,963$ clean rows** (99.80% data retention; Station 42040: $N = 1,445$, Station 41002: $N = 518$).
  2. **Isolated SST Dataset (`cleaned_sst.csv`):** Retains all 518 complete cases of Station 41002 with `WTMP` to evaluate localized sea-surface temperature correlations without corrupting the multi-buoy core sample.

### 6.3 Analyst Plausibility Screening
To identify corrupted telemetry or physical anomalies, heuristic screening boundaries were verified against all active features:
- $WSPD \in [0.0, 50.0]\text{ m/s} \rightarrow$ Observed: $[0.10, 15.30]\text{ m/s}$ (0 violations).
- $GST \in [0.0, 70.0]\text{ m/s} \rightarrow$ Observed: $[0.70, 19.80]\text{ m/s}$ (0 violations).
- $BAR \in [900.0, 1100.0]\text{ hPa} \rightarrow$ Observed: $[1000.70, 1033.20]\text{ hPa}$ (0 violations).
- $ATMP \in [-40.0, 50.0]\text{ °C} \rightarrow$ Observed: $[3.20, 30.90]\text{ °C}$ (0 violations).
- $WTMP \in [-2.0, 40.0]\text{ °C} \rightarrow$ Observed: $[21.70, 29.70]\text{ °C}$ (0 violations).

### 6.4 Cleaned Datasets Catalog

| Filename | Path | Rows ($N$) | Columns | Contained Attributes | Purpose |
|:---|:---|:---:|:---:|:---|:---|
| `raw.csv` | `./data/raw.csv` | 1,967 | 12 | All raw downloaded columns | Ground-truth archive. |
| `cleaned_core.csv` | `./data/cleaned_core.csv` | 1,963 | 8 | `station`, `time (UTC)`, `latitude`, `longitude`, `WSPD`, `GST`, `BAR`, `ATMP` | Primary multi-station pipeline. |
| `cleaned_sst.csv` | `./data/cleaned_sst.csv` | 518 | 9 | Core features + `WTMP` (Station 41002 only) | Localized water temperature study. |
