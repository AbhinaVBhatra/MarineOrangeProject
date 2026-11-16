# Verified Academic References and Annotated Source Notes

**Project Title:** Marine Condition Analysis and Classification Using Data Mining  
**Document:** Verified Literature Citations, IEEE Bibliography, and Source Notes  
**Location:** `./ResearchPaper/References_and_Source_Notes.md`  
**Date:** October 2026  
**Curriculum Context:** B.Tech Computer Science Engineering — Data Mining  

---

## 1. IEEE-Style Master Reference List

```
[1]  National Oceanic and Atmospheric Administration (NOAA) CoastWatch / Environmental Research Division (ERD), "NDBC Standard Meteorological Buoy Data (Dataset ID: cwwcNDBCMet)," NOAA CoastWatch ERDDAP Data Server, 2025. [Online]. Available: https://coastwatch.pfeg.noaa.gov/erddap/tabledap/cwwcNDBCMet.html. Accessed: Oct. 12, 2026.

[2]  National Oceanic and Atmospheric Administration (NOAA) National Data Buoy Center (NDBC), "NDBC Moored Buoy and C-MAN Station Meteorological Data Descriptions and Instrumentation Specifications," National Weather Service, Stennis Space Center, MS, Tech. Doc., 2025. [Online]. Available: https://www.ndbc.noaa.gov/measdes.shtml. Accessed: Oct. 12, 2026.

[3]  E. A. Meindl and G. D. Hamilton, "Programs of the National Data Buoy Center," Bulletin of the American Meteorological Society, vol. 73, no. 7, pp. 985–993, Jul. 1992. doi: 10.1175/1520-0477(1992)073<0985:POTNDB>2.0.CO;2.

[4]  R. Simons, "ERDDAP: A Broker to Oceanographic and Climate Data," in Proc. Ocean Sciences Meeting / NOAA Environmental Software Development, Pacific Grove, CA: NOAA NMFS SWFSC ERD, 2011. [Online]. Available: https://coastwatch.pfeg.noaa.gov/erddap/index.html. Accessed: Oct. 12, 2026.

[5]  W. J. Pierson and L. Moskowitz, "A proposed spectral form for fully developed wind seas based on the similarity theory of S. A. Kitaigorodskii," Journal of Geophysical Research, vol. 69, no. 24, pp. 5181–5190, Dec. 1964. doi: 10.1029/JZ069i024p05181.

[6]  J. Demšar, T. Curk, A. Erjavec, Č. Gorup, T. Hočevar, M. Milutinovič, M. Možina, M. Polajnar, M. Toplak, A. Starič, M. Štajdohar, L. Umek, L. Žagar, J. Žbontar, M. Žitnik, and B. Zupan, "Orange: Data Mining Toolbox in Python," Journal of Machine Learning Research, vol. 14, no. 1, pp. 2349–2353, Aug. 2013. [Online]. Available: http://jmlr.org/papers/v14/demsar13a.html.

[7]  J. MacQueen, "Some methods for classification and analysis of multivariate observations," in Proc. Fifth Berkeley Symp. on Mathematical Statistics and Probability, vol. 1, Berkeley, CA: Univ. of California Press, 1967, pp. 281–297.

[8]  P. J. Rousseeuw, "Silhouettes: A graphical aid to the interpretation and validation of cluster analysis," Journal of Computational and Applied Mathematics, vol. 20, pp. 53–65, Nov. 1987. doi: 10.1016/0377-0427(87)90125-7.

[9]  L. Hubert and P. Arabie, "Comparing partitions," Journal of Classification, vol. 2, no. 1, pp. 193–218, Dec. 1985. doi: 10.1007/BF01908075.

[10] L. Breiman, J. H. Friedman, R. A. Olshen, and C. J. Stone, Classification and Regression Trees. Belmont, CA: Wadsworth & Brooks/Cole Advanced Books & Software, 1984.

[11] L. Breiman, "Random Forests," Machine Learning, vol. 45, no. 1, pp. 5–32, Oct. 2001. doi: 10.1023/A:1010933404324.

[12] D. J. Hand and K. Yu, "Idiot's' Bayes—not so stupid after all?," International Statistical Review, vol. 69, no. 3, pp. 385–398, Dec. 2001. doi: 10.1111/j.1751-5823.2001.tb00465.x.

[13] Indian National Centre for Ocean Information Services (INCOIS), "Potential Fishing Zone (PFZ) Advisory Mission & Methodology," Ministry of Earth Sciences (MoES), Govt. of India, Hyderabad, Tech. Rep., 2025. [Online]. Available: https://incois.gov.in/MarineFisheries/PfzAdvisory. Accessed: Oct. 12, 2026.

[14] World Meteorological Organization (WMO), Guide to Wave Analysis and Forecasting, 3rd ed., WMO-No. 702. Geneva, Switzerland: Secretariat of the World Meteorological Organization, 2018.
```

---

## 2. Detailed Annotated Source Notes

### Source [1]: NOAA CoastWatch ERDDAP Data Server (`cwwcNDBCMet`)
- **Citation:** NOAA CoastWatch/ERD, "NDBC Standard Meteorological Buoy Data," 2025.
- **Verification Status:** Verified against official NOAA CoastWatch portal (`https://coastwatch.pfeg.noaa.gov/erddap/tabledap/cwwcNDBCMet.html`).
- **How Used in Paper:** Primary observational data repository from which the 3-hourly buoy observations covering January 1 to June 30, 2025 were queried. Used to establish exact attribute metadata, physical units, ERDDAP server architecture, and open scientific data licensing.

### Source [2]: NOAA NDBC Measurement Descriptions and Instrumentation Specifications
- **Citation:** NOAA NDBC, "NDBC Moored Buoy and C-MAN Station Meteorological Data Descriptions," 2025.
- **Verification Status:** Verified against NDBC technical documentation (`https://www.ndbc.noaa.gov/measdes.shtml`).
- **How Used in Paper:** Cited for sensor instrumentation standards, sampling intervals, and measurement physics:
  - `WSPD`: 8-minute scalar average of anemometer readings.
  - `GST`: Peak 10-minute 3-second instantaneous gust.
  - `BAR`: Sea-level calibrated aneroid/piezoresistive pressure transducer.
  - `ATMP`: Mast-mounted thermistor/RTD probe in solar radiation shield.
  - `WTMP`: Hull-mounted thermistor at 1-meter depth.
  - Sensor failure modes explaining unmounted wave payloads at coastal/platform stations.

### Source [3]: Meindl & Hamilton (1992) — Programs of the National Data Buoy Center
- **Citation:** E. A. Meindl and G. D. Hamilton, *Bulletin of the American Meteorological Society*, vol. 73, no. 7, pp. 985–993, 1992. doi: 10.1175/1520-0477(1992)073<0985:POTNDB>2.0.CO;2.
- **Verification Status:** Verified via American Meteorological Society (AMS) archives.
- **How Used in Paper:** Cited in the Introduction and Dataset Description to describe the operational mission of the NOAA NDBC moored buoy and C-MAN networks. Explains why buoys deployed in deep ocean vs. shelf/platform stations possess different sensor configurations (explaining why Station 42040 lacked water thermistors and wave accelerometers).

### Source [4]: Simons (2011) — ERDDAP Oceanographic Data Server
- **Citation:** R. Simons, "ERDDAP: A Broker to Oceanographic and Climate Data," 2011.
- **Verification Status:** Verified via NOAA Southwest Fisheries Science Center / ERD documentation.
- **How Used in Paper:** Cited in the Data Acquisition and Preprocessing sections to explain how ERDDAP subsets tabular in-situ marine observations, translates timestamps to standard ISO 8601 UTC, and generates reproducible RESTful queries.

### Source [5]: Pierson & Moskowitz (1964) — Proposed Spectral Form for Fully Developed Wind Seas
- **Citation:** W. J. Pierson and L. Moskowitz, *Journal of Geophysical Research*, vol. 69, no. 24, pp. 5181–5190, 1964. doi: 10.1029/JZ069i024p05181.
- **Verification Status:** Verified via AGU / Wiley JGR archives.
- **How Used in Paper:** Foundational physical oceanographic justification for discretizing wind speed (`WSPD`) as a proxy for sea-state wave energy. The Pierson-Moskowitz equilibrium spectrum establishes that significant wave height is strictly monotonically increasing with sustained wind speed ($H_{m0} \propto U_{10}^2$). This validates that classifying wind condition terciles maps directly to sea-state condition terciles.

### Source [6]: Demšar et al. (2013) — Orange: Data Mining Toolbox in Python
- **Citation:** J. Demšar et al., *Journal of Machine Learning Research*, vol. 14, pp. 2349–2353, 2013.
- **Verification Status:** Verified via JMLR official archives (`http://jmlr.org/papers/v14/demsar13a.html`).
- **How Used in Paper:** Primary software reference for the visual workflow environment, widget implementations (`File`, `Select Columns`, `Preprocess`, `k-Means`, `Tree`, `Random Forest`, `Naive Bayes`, `Test & Score`), and internal domain representation ($X$ matrix vs. meta-attributes, explaining the 34.01% missingness diagnostic).

### Source [7]: MacQueen (1967) — k-Means Clustering
- **Citation:** J. MacQueen, "Some methods for classification and analysis of multivariate observations," in *Proc. 5th Berkeley Symp.*, 1967, pp. 281–297.
- **Verification Status:** Verified via University of California Press archives.
- **How Used in Paper:** Cited in Materials and Methods to explain the mathematical foundation of k-Means partitioning: iteratively minimizing the within-cluster sum of squared Euclidean distances (inertia) between standardized observations and cluster centroids.

### Source [8]: Rousseeuw (1987) — Silhouette Coefficients
- **Citation:** P. J. Rousseeuw, *Journal of Computational and Applied Mathematics*, vol. 20, pp. 53–65, 1987. doi: 10.1016/0377-0427(87)90125-7.
- **Verification Status:** Verified via Elsevier ScienceDirect archives.
- **How Used in Paper:** Mathematical basis for selecting the optimal cluster count $k=2$ (silhouette = 0.3537). Explains the formulation balancing intra-cluster cohesion $a(i)$ and nearest-neighbor cluster separation $b(i)$.

### Source [9]: Hubert & Arabie (1985) — Comparing Partitions (Adjusted Rand Index)
- **Citation:** L. Hubert and P. Arabie, *Journal of Classification*, vol. 2, no. 1, pp. 193–218, 1985. doi: 10.1007/BF01908075.
- **Verification Status:** Verified via SpringerLink archives.
- **How Used in Paper:** Mathematical formulation for validating cluster independence against geographic buoy station identity. An ARI value of $-0.0243$ (near zero) proves that k-Means did not merely split observations by station location coordinates.

### Source [10]: Breiman et al. (1984) — Classification and Regression Trees (CART)
- **Citation:** L. Breiman et al., *Classification and Regression Trees*, 1984.
- **Verification Status:** Verified classic textbook (Wadsworth & Brooks/Cole).
- **How Used in Paper:** Cited in Materials and Methods and Results for the Decision Tree model (max depth = 5, min leaf = 20). Explains recursive binary splitting based on Gini impurity reduction and provides the theoretical foundation for extracting interpretable meteorological rules.

### Source [11]: Breiman (2001) — Random Forests
- **Citation:** L. Breiman, *Machine Learning*, vol. 45, no. 1, pp. 5–32, 2001. doi: 10.1023/A:1010933404324.
- **Verification Status:** Verified via SpringerLink archives.
- **How Used in Paper:** Cited for the ensemble Random Forest model (100 de-correlated trees). Explains bootstrap aggregating (bagging) and random feature subspace selection for reducing model variance on noisy marine observation data.

### Source [12]: Hand & Yu (2001) — Naive Bayes Classification
- **Citation:** D. J. Hand and K. Yu, *International Statistical Review*, vol. 69, no. 3, pp. 385–398, 2001. doi: 10.1111/j.1751-5823.2001.tb00465.x.
- **Verification Status:** Verified via Wiley Online Library.
- **How Used in Paper:** Cited for the Gaussian Naive Bayes baseline. Explains why Naive Bayes remains competitive in environmental classification despite the assumption of class-conditional feature independence.

### Source [13]: Indian National Centre for Ocean Information Services (INCOIS) — PFZ Advisory
- **Citation:** INCOIS, "Potential Fishing Zone (PFZ) Advisory Mission & Methodology," MoES, Govt. of India, 2025.
- **Verification Status:** Verified via INCOIS official portal (`https://incois.gov.in/MarineFisheries/PfzAdvisory`).
- **How Used in Paper:** Cited in the Project Scope and Future Scope sections. Grounds the academic boundary: explains that operational PFZ generation requires multi-sensor satellite remote sensing (Sea Surface Temperature gradients and Chlorophyll-a frontal zones) coupled with oceanic circulation models, properly justifying why PFZ prediction is excluded from this small-scale buoy data mining study.

### Source [14]: World Meteorological Organization (WMO) — Guide to Wave Analysis and Forecasting
- **Citation:** WMO, *Guide to Wave Analysis and Forecasting*, WMO-No. 702, Geneva, Switzerland, 2018.
- **Verification Status:** Verified via WMO Official Library.
- **How Used in Paper:** Cited in the Limitations and Academic Integrity sections to explain the difference between statistical sample terciles derived in an undergraduate project and statutory World Meteorological Organization sea-state codes (Code 3700) or official maritime safety warning thresholds.
