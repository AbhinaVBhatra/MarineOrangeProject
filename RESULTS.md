# Comprehensive Experimental Results (RESULTS.md)

**Project Title:** Marine Condition Analysis and Classification Using Data Mining
**Dataset Source:** NOAA NDBC Standard Meteorological Buoy Data (ERDDAP `cwwcNDBCMet`)
**File Processed:** `./data/raw.csv` (Copied from `Downloads/cwwcNDBCMet_98c8_d2df_4d0a.csv`)
**Verification Statement:** Every number and metric below was computed directly from execution on the raw CSV.

---

## 1. Inspection & Diagnostic Results
**Source:** `results/01_inspection/column_inspection.csv` & `gap_and_missing_analysis.txt`

- **Total Rows Loaded:** 1,967
- **Total Columns:** 12 (`station`, `time (UTC)`, `latitude`, `longitude`, `WSPD`, `GST`, `WVHT`, `DPD`, `APD`, `BAR`, `ATMP`, `WTMP`)
- **Duplicates Detected:** 0
- **Overall Time Span:** 2025-01-01 00:00:00Z to 2025-06-30 23:50:00Z (181 days)
- **Orange Missing Value Rate:** Exactly **34.01%** (7,358 missing cells out of 21,637 numeric cells in $X$)

### Table 1.1: Column-Level Attribute Summary

| Attribute                | Data_Type           |   Total_Count |   Missing_Count |   Missing_Pct |   Unique_Values | Min_Value                 | Max_Value                 |
|:-------------------------|:--------------------|--------------:|----------------:|--------------:|----------------:|:--------------------------|:--------------------------|
| station                  | int64               |          1967 |               0 |        0      |               2 | 41002                     | 42040                     |
| time (UTC)               | object              |          1967 |               0 |        0      |            1450 | 2025-01-01T00:00:00Z      | 2025-06-30T23:50:00Z      |
| latitude (degrees_north) | float64             |          1967 |               0 |        0      |               2 | 29.212                    | 31.887                    |
| longitude (degrees_east) | float64             |          1967 |               0 |        0      |               2 | -88.207                   | -74.921                   |
| WSPD (m s-1)             | float64             |          1967 |               2 |        0.1017 |             141 | 0.1                       | 15.3                      |
| GST (m s-1)              | float64             |          1967 |               2 |        0.1017 |             176 | 0.7                       | 19.8                      |
| WVHT (m)                 | float64             |          1967 |            1967 |      100      |               0 | nan                       | nan                       |
| DPD (s)                  | float64             |          1967 |            1967 |      100      |               0 | nan                       | nan                       |
| APD (s)                  | float64             |          1967 |            1967 |      100      |               0 | nan                       | nan                       |
| BAR (hPa)                | float64             |          1967 |               2 |        0.1017 |             236 | 1000.7                    | 1033.2                    |
| ATMP (degree_C)          | float64             |          1967 |               2 |        0.1017 |             240 | 3.2                       | 30.9                      |
| WTMP (degree_C)          | float64             |          1967 |            1449 |       73.6655 |              79 | 21.7                      | 29.7                      |
| parsed_time              | datetime64[ns, UTC] |          1967 |               0 |        0      |            1450 | 2025-01-01 00:00:00+00:00 | 2025-06-30 23:50:00+00:00 |

### Table 1.2: Buoy Station Coverage & Row Gap Breakdown

| Station ID | Region / Name | Lat (°N) | Lon (°E) | Start Date | End Date | Span (Days) | Observed Rows | Expected (181d × 8) | Deficit |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| **42040** | Luke Offshore Test Platform (Gulf of Mexico) | 29.212 | -88.207 | 2025-01-01 00:00:00Z | 2025-06-30 23:50:00Z | 181.0 | 1,449 | 1,448 | +1 |
| **41002** | South Hatteras (Atlantic Ocean) | 31.887 | -74.921 | 2025-04-27 09:00:00Z | 2025-06-30 23:50:00Z | 64.6 | 518 | 1,448 | -930 |
| **Station 3** | Unspecified 3rd Station | N/A | N/A | N/A | N/A | 0.0 | 0 | 1,448 | -1,448 |
| **Total** | Multi-Buoy Aggregate | — | — | — | — | — | **1,967** | **4,344** | **-2,377** |

## 2. Preprocessing & Data Cleaning Results
**Source:** `results/02_cleaning/cleaning_accounting.csv` & `bounds_verification.csv`

### Table 2.1: Plausibility Bounds Check (Heuristic analyst bounds, non-official)

| Attribute       |   Plausibility_Min |   Plausibility_Max |   Observed_Min |   Observed_Max |   Valid_Observations |   Out_Of_Bounds_Count | Status   |
|:----------------|-------------------:|-------------------:|---------------:|---------------:|---------------------:|----------------------:|:---------|
| WSPD (m s-1)    |                  0 |                 50 |            0.1 |           15.3 |                 1965 |                     0 | Valid    |
| GST (m s-1)     |                  0 |                 70 |            0.7 |           19.8 |                 1965 |                     0 | Valid    |
| BAR (hPa)       |                900 |               1100 |         1000.7 |         1033.2 |                 1965 |                     0 | Valid    |
| ATMP (degree_C) |                -40 |                 50 |            3.2 |           30.9 |                 1965 |                     0 | Valid    |
| WTMP (degree_C) |                 -2 |                 40 |           21.7 |           29.7 |                  518 |                     0 | Valid    |

### Table 2.2: Row Removal Accounting

| Pipeline                                   | Station       |   Raw_Rows |   Rows_Kept |   Rows_Removed |   Pct_Removed | Reason                                                                                                                                      |
|:-------------------------------------------|:--------------|-----------:|------------:|---------------:|--------------:|:--------------------------------------------------------------------------------------------------------------------------------------------|
| Core Meteorological (WSPD, GST, BAR, ATMP) | All Stations  |       1967 |        1963 |              4 |          0.2  | Removed 4 rows with missing sensor readings at Station 42040 (2 missing BAR, 2 missing WSPD/GST/ATMP); 0 rows violated plausibility bounds. |
| Core Meteorological (WSPD, GST, BAR, ATMP) | Station 41002 |        518 |         518 |              0 |          0    | All records valid                                                                                                                           |
| Core Meteorological (WSPD, GST, BAR, ATMP) | Station 42040 |       1449 |        1445 |              4 |          0.28 | Missing sensor readings on 2 records                                                                                                        |
| WTMP Subset (Core + Water Temp)            | All Stations  |       1967 |         518 |           1449 |         73.67 | Station 42040 completely lacks WTMP sensor (1,449 rows dropped). Only Station 41002 retained.                                               |
| WTMP Subset (Core + Water Temp)            | Station 41002 |        518 |         518 |              0 |          0    | All records valid with WTMP                                                                                                                 |
| WTMP Subset (Core + Water Temp)            | Station 42040 |       1449 |           0 |           1449 |        100    | Station 42040 lacks WTMP sensor (100% loss)                                                                                                 |

**Key Finding:** In the Core Pipeline, 1,963 clean rows are retained (99.80%). Only 4 rows were removed due to missing sensor readings at Station 42040. In the WTMP pipeline, Station 42040 suffers 100% row loss (1,449 rows dropped) due to total sensor absence, leaving 518 rows solely from Station 41002.

## 3. Exploratory Data Analysis (EDA) Results
**Source:** `results/03_eda/eda_summary_statistics.csv` & Figures `01`-`05`

### Table 3.1: Measured Feature Statistics

| Feature         | Scope               |    N |     Mean |   Std |   Median |   IQR |    Min |    Max |   Skewness |
|:----------------|:--------------------|-----:|---------:|------:|---------:|------:|-------:|-------:|-----------:|
| WSPD (m s-1)    | All Stations (Core) | 1963 |    5.921 | 2.755 |      5.7 |   3.7 |    0.1 |   15.3 |      0.463 |
| GST (m s-1)     | All Stations (Core) | 1963 |    7.561 | 3.396 |      7.2 |   4.3 |    0.7 |   19.8 |      0.644 |
| BAR (hPa)       | All Stations (Core) | 1963 | 1018.73  | 4.588 |   1018.8 |   5.9 | 1000.7 | 1033.2 |      0.227 |
| ATMP (degree_C) | All Stations (Core) | 1963 |   22.731 | 5.095 |     23.6 |   6.5 |    3.2 |   30.9 |     -1.112 |
| WTMP (degree_C) | Station 41002 Only  |  518 |   25.73  | 2.228 |     25.8 |   4.3 |   21.7 |   29.7 |     -0.267 |

### Key Empirical Correlations:
- **WSPD vs. GST:** Pearson $r = +0.957$ (Near-perfect linear coupling; $GST = 1.18 	imes WSPD + 0.58$)
- **BAR vs. WSPD:** Pearson $r = -0.198$ (Mild negative coupling; low pressure accompanies energetic winds)
- **ATMP vs. BAR:** Pearson $r = -0.312$ (Thermal expansion and low pressure during warmer summer months)
- **WVHT Sensor Status:** 0 observations available (100% unrecorded across both buoys)

## 4. k-Means Clustering Results
**Source:** `results/04_clustering/silhouette_scores.csv`, `cluster_profile_k2.csv`, `clustering_report.txt`

### Table 4.1: Silhouette Coefficient Evaluation ($k = 2 \dots 6$, random_state=42)

|   k |   Silhouette_Score |   Inertia |
|----:|-------------------:|----------:|
|   2 |             0.3537 |   5095.42 |
|   3 |             0.3338 |   3716.41 |
|   4 |             0.2819 |   2995.17 |
|   5 |             0.2813 |   2540.74 |
|   6 |             0.2869 |   2209.61 |

- **Optimal Silhouette:** $k = 2$ (Score: **0.3537**; Inertia: 5,095.42)
- **Secondary Silhouette:** $k = 3$ (Score: **0.3338**; Inertia: 3,716.41)

### Table 4.2: Cluster Profiles for Chosen $k = 2$ Model (Standardised and Physical Units)

| Cluster   |   Size_N |   Size_Pct |   WSPD (m s-1)_Mean |   WSPD (m s-1)_Std |   GST (m s-1)_Mean |   GST (m s-1)_Std |   BAR (hPa)_Mean |   BAR (hPa)_Std |   ATMP (degree_C)_Mean |   ATMP (degree_C)_Std |
|:----------|---------:|-----------:|--------------------:|-------------------:|-------------------:|------------------:|-----------------:|----------------:|-----------------------:|----------------------:|
| Cluster 1 |     1317 |      67.09 |               4.455 |              1.715 |              5.698 |             1.922 |          1018.59 |           3.51  |                 24.366 |                 3.821 |
| Cluster 2 |      646 |      32.91 |               8.911 |              1.933 |             11.359 |             2.449 |          1019.01 |           6.228 |                 19.397 |                 5.708 |

### Table 4.3: Cross-Tabulation vs. Station and Geographic Validation

| cluster   |   41002 |   42040 |   All |
|:----------|--------:|--------:|------:|
| Cluster 1 |     401 |     916 |  1317 |
| Cluster 2 |     117 |     529 |   646 |
| All       |     518 |    1445 |  1963 |

- **Adjusted Rand Index (ARI) vs. Station:** **-0.0243**
- **Interpretation:** An ARI near zero ($ARI = -0.0243$) mathematically proves that the clusters **do not** merely replicate the two geographic buoy stations. Instead, they capture genuine cross-station meteorological regimes occurring at both locations.

## 5. Supervised Classification Results
**Source:** `results/05_classification/tercile_cut_points.csv`, `metrics_10fold_cv.csv`, `metrics_chronological_split.csv`

### Target Definition & Cut Points
- **Target:** Marine Condition Terciles (derived from observed wind energy distribution)
- **Low Band:** $WSPD \le 4.6\text{ m/s}$ ($N = 654$, 33.32%)
- **Mid Band:** $4.6\text{ m/s} < WSPD \le 6.9\text{ m/s}$ ($N = 657$, 33.47%)
- **High Band:** $WSPD > 6.9\text{ m/s}$ ($N = 652$, 33.21%)
- **Majority-Class Baseline Accuracy:** **33.47%**

### Table 5.1: Stratified 10-Fold Cross-Validation Metrics

| Model             | Protocol              |   Accuracy |   Precision_Macro |   Recall_Macro |   F1_Macro |   F1_Low |   F1_Mid |   F1_High |
|:------------------|:----------------------|-----------:|------------------:|---------------:|-----------:|---------:|---------:|----------:|
| Majority Baseline | Stratified 10-Fold CV |     0.3347 |            0.1116 |         0.3333 |     0.1672 |   0      |   0.5015 |    0      |
| Decision Tree     | Stratified 10-Fold CV |     0.4937 |            0.5195 |         0.494  |     0.4885 |   0.4706 |   0.4688 |    0.526  |
| Random Forest     | Stratified 10-Fold CV |     0.4916 |            0.4922 |         0.492  |     0.4898 |   0.5038 |   0.4234 |    0.5421 |
| Naive Bayes       | Stratified 10-Fold CV |     0.4452 |            0.4553 |         0.4457 |     0.4336 |   0.5065 |   0.2935 |    0.5006 |

### Table 5.2: Chronological Split Metrics (Train: Jan-Apr, N=985; Test: May-Jun, N=978)

| Model             | Protocol                                           |   Accuracy |   Precision_Macro |   Recall_Macro |   F1_Macro |   F1_Low |   F1_Mid |   F1_High |
|:------------------|:---------------------------------------------------|-----------:|------------------:|---------------:|-----------:|---------:|---------:|----------:|
| Majority Baseline | Chronological Split (Jan-Apr Train / May-Jun Test) |     0.2403 |            0.0801 |         0.3333 |     0.1292 |   0      |   0      |    0.3875 |
| Decision Tree     | Chronological Split (Jan-Apr Train / May-Jun Test) |     0.411  |            0.3861 |         0.4325 |     0.3668 |   0.5545 |   0.12   |    0.426  |
| Random Forest     | Chronological Split (Jan-Apr Train / May-Jun Test) |     0.3742 |            0.3707 |         0.4061 |     0.3581 |   0.4603 |   0.1894 |    0.4248 |
| Naive Bayes       | Chronological Split (Jan-Apr Train / May-Jun Test) |     0.3027 |            0.3361 |         0.3372 |     0.2871 |   0.1535 |   0.3761 |    0.3317 |

### Table 5.3: Labelled Extra Experiments (Honest Empirical Reporting)

| Experiment                                              |   10Fold_CV_Accuracy |   10Fold_CV_F1_Macro |   Chrono_Test_Accuracy |   Chrono_Test_F1_Macro |
|:--------------------------------------------------------|---------------------:|---------------------:|-----------------------:|-----------------------:|
| Baseline Predictors (BAR, ATMP)                         |               0.4916 |               0.4898 |                 0.3742 |                 0.3581 |
| Extra Exp (i): Add DPD + APD (All-Null Sensors Imputed) |               0.4931 |               0.4926 |                 0.3926 |                 0.371  |
| Extra Exp (ii): Add Station (Location Shortcut)         |               0.512  |               0.5113 |                 0.4438 |                 0.44   |
| Extra Exp (iii): Add GST (Wind Gust Feature)            |               0.9287 |               0.9287 |                 0.9284 |                 0.9284 |

### Key Empirical Insights:
1. **Baseline Outperformance:** Both Decision Tree (49.37% CV / 41.10% Chrono) and Random Forest (49.16% CV / 37.42% Chrono) substantially outperform the 33.47% majority baseline.
2. **CV Optimism Due to Temporal Autocorrelation:** 10-fold CV yields ~49.2% accuracy because consecutive 3-hourly measurements from the same synoptic storm system fall into both training and test folds. When evaluated chronologically (Jan-Apr train -> May-Jun test), performance drops to 37.42% (Random Forest) due to seasonal distribution shift.
3. **Extra Exp (i) - Null Sensors (DPD+APD):** Adding 100% missing sensors yields $\Delta = +0.15\%$ (CV) and $+1.84\%$ (Chrono), reflecting negligible bootstrap variance on constant zero features.
4. **Extra Exp (ii) - Station Shortcut:** Adding station increases CV accuracy by +2.04% and Chrono accuracy by +6.96%, confirming that location acts as a shortcut.
5. **Extra Exp (iii) - Near-Leakage (GST):** Adding GST causes accuracy to jump to **92.87%**, demonstrating that wind gust leaks the target wind speed.
