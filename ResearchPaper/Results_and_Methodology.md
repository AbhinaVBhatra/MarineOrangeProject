# Comprehensive Results, Methodology, and Experimental Evidence

**Project Title:** Marine Condition Analysis and Classification Using Data Mining  
**Document:** Methodological Framework, Experimental Settings, and Verified Results  
**Location:** `./ResearchPaper/Results_and_Methodology.md`  
**Date:** October 2026  
**Curriculum Context:** B.Tech Computer Science Engineering — Data Mining  

---

## 1. Methodological Framework: CRISP-DM

The research methodology follows the standard Cross-Industry Standard Process for Data Mining (CRISP-DM) framework adapted for continuous environmental telemetry:

```
[ Domain Understanding & Research Questions ]
                      │
                      v
     [ Data Understanding & Forensic Audit ]
                      │
                      v
   [ Data Preprocessing & Threshold Cleaning ]
                      │
                      v
      [ Exploratory Data Analysis (EDA) ]
                      │
         ┌────────────┴────────────┐
         │                         │
         v                         v
[ k-Means Clustering ]   [ Supervised Classification ]
(Standardize, k=2..6,    (WSPD Terciles, BAR & ATMP,
Silhouette, ARI Test)    10-Fold CV vs Chrono Split)
         │                         │
         └────────────┬────────────┘
                      │
                      v
      [ Evaluation & Scientific Synthesis ]
```

---

## 2. Research Questions

### Main Research Question
* **RQ1:** Can data mining techniques uncover meaningful physical patterns in in-situ marine meteorological observations and classify observed marine condition regimes using atmospheric surface predictors without location shortcuts or data leakage?

### Supporting Research Questions
* **RQ2 (Unsupervised Clustering):** Does k-Means clustering identify distinct, meteorologically coherent marine weather regimes across multi-buoy observations, and do these clusters represent shared physical states rather than geographic station coordinates?
* **RQ3 (Supervised Classification):** To what extent can independent barometric pressure and air temperature measurements classify discretized marine condition terciles above baseline levels?
* **RQ4 (Temporal Generalization):** What is the quantitative impact of temporal autocorrelation on model evaluation when comparing standard randomized 10-fold cross-validation against a forward chronological split?

---

## 3. Exploratory Data Analysis (EDA) Empirical Results

### 3.1 Descriptive Statistics
Analysis of $N = 1,963$ clean observations across both buoy stations:

| Feature | Scope | $N$ | Mean | Std Dev | Median | IQR | Min | Max | Skewness |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `WSPD (m s-1)` | All Stations | 1,963 | 5.921 | 2.755 | 5.700 | 3.700 | 0.100 | 15.300 | +0.463 |
| `GST (m s-1)` | All Stations | 1,963 | 7.561 | 3.396 | 7.200 | 4.300 | 0.700 | 19.800 | +0.644 |
| `BAR (hPa)` | All Stations | 1,963 | 1018.725 | 4.588 | 1018.800 | 5.900 | 1000.700 | 1033.200 | +0.227 |
| `ATMP (degree_C)` | All Stations | 1,963 | 22.731 | 5.095 | 23.600 | 6.500 | 3.200 | 30.900 | -1.112 |
| `WTMP (degree_C)` | Station 41002 | 518 | 25.730 | 2.228 | 25.800 | 4.300 | 21.700 | 29.700 | -0.267 |

### 3.2 Key Physical and Statistical Findings
1. **Near-Perfect Linear Coupling between Wind and Gust:**
   $$\text{GST} = 1.18 \times \text{WSPD} + 0.58 \quad (r = +0.957, \ p < 0.001)$$
   Wind gust exhibits a near-deterministic physical scaling with sustained wind speed. Including `GST` in predictive models of wind conditions constitutes direct near-leakage.
2. **Barometric Pressure Depressions:**
   Pearson correlation between `BAR` and `WSPD` is $r = -0.198$. Energetic wind speed peaks (>10 m/s) systematically coincide with transient barometric depressions ($<1015$ hPa), consistent with extratropical cyclonic passages.
3. **Thermal Regimes Across Stations:**
   Station 42040 (Gulf of Mexico) displays high temperature variability (3.2 °C to 30.9 °C) reflecting continental air mass advection. Station 41002 (Atlantic, observed April–June) is constrained to warm maritime conditions (mean 23.36 °C).
4. **Significant Wave Height Non-Reporting:**
   The wave height variable `WVHT (m)` contains exactly **zero observations (100% missing)**. Direct classification of wave height is empirically impossible on this raw dataset.

---

## 4. Unsupervised k-Means Clustering Results

### 4.1 Preprocessing and Feature Standardization
Clustering features (`WSPD`, `GST`, `BAR`, `ATMP`) were standardized using z-score normalization ($\mu = 0, \sigma = 1$) to eliminate scale dominance (e.g., pressure $\approx 1018$ hPa vs. wind $\approx 5.9$ m/s). Random seed was fixed at 42.

### 4.2 Silhouette and Inertia Optimization ($k = 2 \dots 6$)

| Clusters ($k$) | Average Silhouette Score | Within-Cluster Inertia | Evaluation & Selection Notes |
|:---:|:---:|:---:|:---|
| **$k = 2$** | **0.3537** | **5,095.42** | **Optimal global silhouette coefficient. Clean physical interpretability.** |
| **$k = 3$** | 0.3338 | 3,716.41 | Secondary silhouette peak; divides calm, moderate, and turbulent regimes. |
| **$k = 4$** | 0.2819 | 2,995.17 | Moderate degradation in cluster cohesion and separation. |
| **$k = 5$** | 0.2813 | 2,540.74 | Low silhouette; cluster fragmentation observed. |
| **$k = 6$** | 0.2869 | 2,209.61 | Slight leveling; over-partitioned regimes. |

### 4.3 Profile of Chosen $k = 2$ Clusters

| Cluster Label | Count ($N$) | Percentage | Mean WSPD ($\text{m/s}$) | Mean GST ($\text{m/s}$) | Mean BAR ($\text{hPa}$) | Mean ATMP (°C) | Physical Regime Characterization |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| **Cluster 1** | 1,317 | 67.09% | $4.46 \pm 1.72$ | $5.70 \pm 1.92$ | $1018.59 \pm 3.51$ | $24.37 \pm 3.82$ | **Tranquil / Warm Regime:** Moderate surface winds, stable barometric pressure, elevated ambient temperatures. |
| **Cluster 2** | 646 | 32.91% | $8.91 \pm 1.93$ | $11.36 \pm 2.45$ | $1019.01 \pm 6.23$ | $19.40 \pm 5.71$ | **Energetic / Cool Regime:** High sustained winds, elevated gusts, cooler temperatures, higher barometric variance. |

### 4.4 Standardized Centroids ($k = 2$)

| Cluster | WSPD ($z$) | GST ($z$) | BAR ($z$) | ATMP ($z$) |
|:---|:---:|:---:|:---:|:---:|
| **Cluster 1** | -0.5323 | -0.5486 | -0.0298 | +0.3209 |
| **Cluster 2** | +1.0846 | +1.1179 | +0.0608 | -0.6539 |

### 4.5 Adjusted Rand Index (ARI) Cross-Station Validation
Contingency table cross-tabulating $k = 2$ cluster assignments against buoy station:

| Cluster | Station 41002 (Atlantic) | Station 42040 (Gulf of Mexico) | Total |
|:---|:---:|:---:|:---:|
| **Cluster 1** | 401 | 916 | 1,317 |
| **Cluster 2** | 117 | 529 | 646 |
| **Total** | 518 | 1,445 | 1,963 |

$$\text{Adjusted Rand Index (ARI vs. Station)} = \mathbf{-0.0243}$$

**Scientific Significance:** Because the ARI is near zero ($-0.0243$), the clustering model **does not recreate geographic buoy stations**. Both stations experience both Cluster 1 and Cluster 2 conditions. The model captures genuine cross-basin meteorological regimes rather than spatial coordinates.

---

## 5. Supervised Classification Results

### 5.1 Target Formulation and Equal-Frequency Terciles
Under oceanographic wave generation theory (Pierson-Moskowitz empirical formulation: $H_{m0} \propto U_{10}^2$), significant wave height scales monotonically with surface wind speed. Discretizing wind speed establishes **Marine Condition Terciles**:
- **Low Band:** $\text{WSPD} \le 4.60\text{ m/s}$ ($N = 654$, 33.32%)
- **Mid Band:** $4.60\text{ m/s} < \text{WSPD} \le 6.90\text{ m/s}$ ($N = 657$, 33.47%)
- **High Band:** $\text{WSPD} > 6.90\text{ m/s}$ ($N = 652$, 33.21%)
- **Total Valid Observations:** $N = 1,963$
- **Majority Baseline Accuracy:** Exactly **33.47%**

### 5.2 Predictor Quarantine
To guarantee academic integrity and prevent leakage:
- `WSPD (m s-1)`: EXCLUDED (Target leakage).
- `GST (m s-1)`: EXCLUDED (Near-leakage wind gust; $r = 0.957$).
- `station`, `latitude`, `longitude`: EXCLUDED (Location shortcuts).
- **Active Predictors:** `BAR (hPa)` (barometric pressure) and `ATMP (degree_C)` (air temperature).

### 5.3 Comparative Performance Benchmark

| Model | Evaluation Protocol | Accuracy | Precision (Macro) | Recall (Macro) | F1-Score (Macro) | F1 (Low) | F1 (Mid) | F1 (High) |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Majority Baseline** | Stratified 10-Fold CV | 33.47% | 0.1116 | 0.3333 | 0.1672 | 0.0000 | 0.5015 | 0.0000 |
| **Decision Tree** (depth 5, leaf 20) | Stratified 10-Fold CV | **49.37%** | **0.5195** | **0.4940** | **0.4885** | 0.4706 | 0.4688 | 0.5260 |
| **Random Forest** (100 trees) | Stratified 10-Fold CV | **49.16%** | **0.4922** | **0.4920** | **0.4898** | 0.5038 | 0.4234 | 0.5421 |
| **Gaussian Naive Bayes** | Stratified 10-Fold CV | 44.52% | 0.4553 | 0.4457 | 0.4336 | 0.5065 | 0.2935 | 0.5006 |
| **Majority Baseline** | Chronological Split | 24.03% | 0.0801 | 0.3333 | 0.1292 | 0.0000 | 0.0000 | 0.3875 |
| **Decision Tree** (depth 5, leaf 20) | Chronological Split | **41.10%** | **0.3861** | **0.4325** | **0.3668** | 0.5545 | 0.1200 | 0.4260 |
| **Random Forest** (100 trees) | Chronological Split | **37.42%** | **0.3707** | **0.4061** | **0.3581** | 0.4603 | 0.1894 | 0.4248 |
| **Gaussian Naive Bayes** | Chronological Split | 30.27% | 0.3361 | 0.3372 | 0.2871 | 0.1535 | 0.3761 | 0.3317 |

*Note: Chronological split trains on historical months January through April ($N = 985$) and tests on forward future months May through June ($N = 978$).*

### 5.4 Confusion Matrices

#### Stratified 10-Fold CV Aggregated Confusion Matrices ($N = 1,963$)

```
Decision Tree (10-Fold CV):
               Predicted Low   Predicted Mid   Predicted High
True Low            328             185             141
True Mid            184             302             171
True High           138             175             339

Random Forest (10-Fold CV):
               Predicted Low   Predicted Mid   Predicted High
True Low            336             178             140
True Mid            206             257             194
True High           136             144             372

Gaussian Naive Bayes (10-Fold CV):
               Predicted Low   Predicted Mid   Predicted High
True Low            350              68             236
True Mid            276             145             236
True High           170             103             379
```

#### Chronological Split Confusion Matrices ($N = 978$ Test Records)

```
Decision Tree (Chrono Split):
               Predicted Low   Predicted Mid   Predicted High
True Low            275              20             110
True Mid            214              36             163
True High           155              14              96

Random Forest (Chrono Split):
               Predicted Low   Predicted Mid   Predicted High
True Low            232              48             125
True Mid            216              50             147
True High           146              35              84
```

---

## 6. Interpretable Decision Tree Rules

Exported rules from the Decision Tree model (max depth = 5, min leaf = 20) fitted on the historical baseline (January–April, $N = 985$):

```
|--- BAR (hPa) <= 1016.75
|   |--- ATMP (degree_C) <= 17.90
|   |   |--- class: High
|   |--- ATMP (degree_C) >  17.90
|   |   |--- BAR (hPa) <= 1009.95
|   |   |   |--- class: High
|   |   |--- BAR (hPa) >  1009.95
|   |   |   |--- ATMP (degree_C) <= 23.75
|   |   |   |   |--- class: High
|   |   |   |--- ATMP (degree_C) >  23.75
|   |   |   |   |--- class: High
|--- BAR (hPa) >  1016.75
|   |--- ATMP (degree_C) <= 11.25
|   |   |--- BAR (hPa) <= 1026.15
|   |   |   |--- class: High
|   |   |--- BAR (hPa) >  1026.15
|   |   |   |--- class: High
|   |--- ATMP (degree_C) >  11.25
|   |   |--- ATMP (degree_C) <= 21.75
|   |   |   |--- BAR (hPa) <= 1025.00
|   |   |   |   |--- BAR (hPa) <= 1021.55
|   |   |   |   |   |--- class: High
|   |   |   |   |--- BAR (hPa) >  1021.55
|   |   |   |   |   |--- class: Low
|   |   |   |--- BAR (hPa) >  1025.00
|   |   |   |   |--- BAR (hPa) <= 1025.95
|   |   |   |   |   |--- class: Mid
|   |   |   |   |--- BAR (hPa) >  1025.95
|   |   |   |   |   |--- class: High
|   |   |--- ATMP (degree_C) >  21.75
|   |   |   |--- ATMP (degree_C) <= 24.25
|   |   |   |   |--- class: Mid
|   |   |   |--- ATMP (degree_C) >  24.25
|   |   |   |   |--- class: Low
```

### Physical Meteorological Synthesis of Tree Splits
1. **Low Barometric Depression ($\text{BAR} \le 1016.75\text{ hPa}$):** Predicts class `High` (turbulent wind energy). Accurately captures cyclonic storms where barometric pressure drops while wind speeds spike.
2. **Warm High-Pressure Anticyclone ($\text{BAR} > 1016.75\text{ hPa}$ and $\text{ATMP} > 24.25\text{ °C}$):** Predicts class `Low` (tranquil marine conditions). Captures stable subtropical summer ridge conditions.
3. **Transitional Regimes ($1016.75 < \text{BAR} \le 1025.95\text{ hPa}$ and $21.75 < \text{ATMP} \le 24.25\text{ °C}$):** Predicts class `Mid` (moderate marine conditions).

---

## 7. Labelled Extra Experiments (Honest Empirical Reporting)

To explicitly investigate the risks of data leakage and zero-variance features, three controlled experiments were conducted using the Random Forest classifier (100 trees):

| Experiment Configuration | Active Predictors | 10-Fold CV Accuracy | 10-Fold CV Macro F1 | Chronological Test Accuracy | Chronological Test Macro F1 | Empirical Scientific Interpretation |
|:---|:---|:---:|:---:|:---:|:---:|:---|
| **Baseline Predictors** | `BAR`, `ATMP` | **49.16%** | **0.4898** | **37.42%** | **0.3581** | Legitimate non-leaking atmospheric baseline. |
| **(i) Add DPD + APD** | `BAR`, `ATMP`, `DPD_imp`, `APD_imp` | **49.31%** | **0.4926** | **39.26%** | **0.3710** | Null sensors imputed with constants (zero variance). $\Delta = +0.15\%$ in CV is pure bootstrap variance; constant features provide zero entropy reduction. |
| **(ii) Add Station** | `BAR`, `ATMP`, `station_binary` | **51.20%** | **0.5113** | **44.38%** | **0.4400** | Location shortcut. Station ID allows model to memorize regional climatology rather than learning atmospheric physics. |
| **(iii) Add GST** | `BAR`, `ATMP`, `GST` | **92.87%** | **0.9287** | **92.84%** | **0.9284** | Severe target near-leakage. Concurrent wind gust is physically co-dependent ($r=0.957$) with wind speed, artificially inflating accuracy. |

---

## 8. Limitations and Academic Integrity Disclaimers

1. **Geographic Limitation:** Data is restricted entirely to United States territorial waters (Atlantic and Gulf of Mexico). Findings cannot be extrapolated to Indian waters.
2. **Temporal Constraint:** The study spans only 6 months, capturing a single winter-to-summer transition rather than multi-year climatological cycles.
3. **Station Attrition:** Captures only 2 stations rather than 3, with Station 41002 suffering an extensive 116-day gap.
4. **Derived Tercile Target:** The classification target represents statistical terciles of this observational sample, NOT certified World Meteorological Organization (WMO) sea-state codes or official maritime safety thresholds.
5. **Operational Use Prohibition:** Models must NEVER be deployed for autonomous vessel routing, marine navigation clearance, or storm life-safety alerts.
