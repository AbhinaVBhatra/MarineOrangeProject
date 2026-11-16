import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_slide_header(slide, title_text, category="DATA MINING COLLEGE PROJECT | B.TECH"):
    # Header banner shape
    header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.5), Inches(1.1))
    tf = header_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p_cat = tf.paragraphs[0]
    p_cat.text = category.upper()
    p_cat.font.name = 'Arial'
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = RGBColor(0, 102, 204) # Electric Blue
    
    p_title = tf.add_paragraph()
    p_title.text = title_text
    p_title.font.name = 'Arial'
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = RGBColor(16, 44, 87) # Deep Navy

def add_card(slide, left, top, width, height, title, body_bullets, bg_rgb=(245, 248, 252), border_rgb=(200, 215, 235)):
    # Add rectangle
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(*bg_rgb)
    shape.line.color.rgb = RGBColor(*border_rgb)
    shape.line.width = Pt(1.5)

    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.2)
    tf.margin_bottom = Inches(0.1)

    p_t = tf.paragraphs[0]
    p_t.text = title
    p_t.font.name = 'Arial'
    p_t.font.size = Pt(13)
    p_t.font.bold = True
    p_t.font.color.rgb = RGBColor(16, 44, 87)
    p_t.space_after = Pt(8)

    for bullet in body_bullets:
        p = tf.add_paragraph()
        p.text = f"• {bullet}"
        p.font.name = 'Arial'
        p.font.size = Pt(11)
        p.font.color.rgb = RGBColor(40, 40, 40)
        p.space_after = Pt(5)

def generate_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # -------------------------------------------------------------
    # SLIDE 1: Title Slide
    # -------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    # Background accent
    bg = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg.fill.solid(); bg.fill.fore_color.rgb = RGBColor(248, 250, 253); bg.line.fill.background()

    # Title card
    tb = s1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11.0), Inches(4.0))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "MARINE CONDITION ANALYSIS AND CLASSIFICATION\nUSING DATA MINING"
    p.font.name = 'Arial'; p.font.size = Pt(32); p.font.bold = True; p.font.color.rgb = RGBColor(16, 44, 87)
    p.space_after = Pt(14)

    p2 = tf.add_paragraph()
    p2.text = "An Empirical Investigation of In-Situ NOAA NDBC Buoy Telemetry (CRISP-DM Framework)"
    p2.font.name = 'Arial'; p2.font.size = Pt(16); p2.font.italic = True; p2.font.color.rgb = RGBColor(0, 102, 204)
    p2.space_after = Pt(28)

    p3 = tf.add_paragraph()
    p3.text = "Third-Year B.Tech Data Mining College Project Examination\nAcademic Context: Inspired by SIH26176 Marine Intelligence Platform Concepts\nData Source: NOAA CoastWatch ERDDAP (cwwcNDBCMet) | US Marine Waters Only"
    p3.font.name = 'Arial'; p3.font.size = Pt(12); p3.font.color.rgb = RGBColor(80, 80, 80)

    # -------------------------------------------------------------
    # SLIDE 2: Project Context & Scope Boundaries
    # -------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    create_slide_header(s2, "Project Context, Motivation & Strict Scope Boundaries")
    add_card(s2, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Research Motivation & Core Question",
             ["Marine Situational Awareness: Coastal operations, fishing fleets, and offshore structures require timely classification of marine weather regimes.",
              "Core Research Question: Can data mining discover meaningful physical patterns in in-situ meteorological buoy observations and accurately classify marine conditions without location shortcuts or data leakage?",
              "Grounded in Real Telemetry: Evaluated on continuous 3-hourly marine buoy telemetry from the National Data Buoy Center (NDBC)."])
    add_card(s2, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Academic Scope vs. SIH Platform (Strict Boundaries)",
             ["Inspired by SIH26176: Problem statement envisions an end-to-end Agentic AI marine intelligence platform.",
              "Deliberately Reduced Curriculum Scope: Focus is 100% on core data mining (CRISP-DM: Data Inspection, Preprocessing, EDA, k-Means Clustering, and Supervised Classification).",
              "Demarcated as Future Scope: Autonomous multi-agent pipelines, chatbot conversational agents, emergency alerts, route optimization, and satellite-based Potential Fishing Zone (PFZ) advisory generation.",
              "Academic Honesty: No unverified claims; all results derived strictly from executed code."],
             bg_rgb=(255, 250, 240), border_rgb=(240, 210, 160))

    # -------------------------------------------------------------
    # SLIDE 3: Inspection: Resolving the 1,967 vs ~4,300 Row Gap
    # -------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    create_slide_header(s3, "Forensic Data Inspection: Resolving the Row Count Gap")
    add_card(s3, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "The Expected vs. Observed Deficit",
             ["Theoretical Expectation (~4,300 Rows):\n  181 calendar days (Jan 1 - Jun 30, 2025)\n  × 8 readings/day (3-hourly)\n  = 1,448 timestamps per station\n  × 3 stations = 4,344 expected records.",
              "Actual CSV Shape: Exactly 1,967 rows across 12 attributes.",
              "Root Cause 1 - Missing Station:\n  Only 2 stations were included in the query (Station 42040 and Station 41002). The 3rd station was completely absent.",
              "Deficit from Station Omission: -1,448 rows."])
    add_card(s3, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Station-Level Timespan Analysis",
             ["Station 42040 (Luke Offshore, Gulf of Mexico):\n  • 1,449 rows observed (2025-01-01 to 2025-06-30)\n  • 181.0 days covered -> Full 6-month historical baseline.",
              "Station 41002 (South Hatteras, Atlantic Ocean):\n  • 518 rows observed (2025-04-27 to 2025-06-30)\n  • Only 64.6 days covered -> Truncated deployment!\n  • 116.4 days missing from winter/early spring (-930 rows).",
              "Total Empirical Rows: 1,449 + 518 = 1,967 rows.",
              "Defensible Decision: Work strictly with the 1,967 real records; zero synthetic data fabrication."])

    # -------------------------------------------------------------
    # SLIDE 4: Demystifying Orange's 34% Missing Values Diagnostic
    # -------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    create_slide_header(s4, "Demystifying Orange's '34% Missing Values' Diagnostic")
    add_card(s4, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Orange's Internal Domain Representation",
             ["When raw.csv is loaded into Orange, Orange classifies the 11 numeric attributes as feature domain X (treating 'time (UTC)' as meta).",
              "Total Feature Matrix Cells: 1,967 rows × 11 numeric features = 21,637 cells.",
              "Total Missing Feature Cells: Exactly 7,358 missing values.",
              "Mathematical Missingness Rate:\n  (7,358 / 21,637) × 100 = 34.0066% (34.01%).",
              "Examiner Significance: Demonstrates full technical command of Orange's internal data engine."])
    add_card(s4, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Column-Level Attribution of Missingness",
             ["WVHT (m), DPD (s), APD (s) -> 100.0% Missing:\n  1,967 / 1,967 cells unrecorded. Accelerometer wave payloads were completely uninstalled or offline.",
              "WTMP (°C) -> 73.67% Missing:\n  1,449 / 1,967 cells missing. Station 42040 completely lacks a water temperature sensor (recorded only at 41002).",
              "WSPD, GST, BAR, ATMP -> 0.10% Missing:\n  Only 2 readings each missing across 4 distinct records at Station 42040.",
              "Key Takeaway: 34% missingness is driven by 3 empty wave columns and 1 partially unequipped station."])

    # -------------------------------------------------------------
    # SLIDE 5: Preprocessing & Plausibility Bounds
    # -------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    create_slide_header(s5, "Data Preprocessing: Thresholds & Geographic Trade-Offs")
    add_card(s5, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Cleaning Rules & Plausibility Verification",
             ["Missingness Threshold (50.0% Rule):\n  Attributes with >50% missingness dropped. WVHT, DPD, and APD (100% missing) dropped universally.",
              "Analyst Plausibility Screening (Heuristic, Non-Official):\n  • WSPD: [0, 50] m/s -> Observed: [0.1, 15.3] m/s (0 violations)\n  • GST: [0, 70] m/s -> Observed: [0.7, 19.8] m/s (0 violations)\n  • BAR: [900, 1100] hPa -> Observed: [1000.7, 1033.2] (0 violations)\n  • ATMP: [-40, 50] °C -> Observed: [3.2, 30.9] °C (0 violations)\n  • WTMP: [-2, 40] °C -> Observed: [21.7, 29.7] °C (0 violations)",
              "Sensor Outage Filtering: Removed 4 records with missing readings at Station 42040."])
    add_card(s5, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "The WTMP Geographic Preservation Dilemma",
             ["The Trade-Off: Requiring water temperature (WTMP) forces complete-case removal of ALL 1,449 rows of Station 42040 (100% loss).",
              "Consequence: Collapses multi-buoy dataset into a single-buoy Atlantic sample (N=518), destroying spatial validity.",
              "Defensible Solution Adopted:\n  1. Core Pipeline (Primary): Retain WSPD, GST, BAR, ATMP across both stations (N=1,963 clean rows, 99.80% retained).\n  2. SST Pipeline (Isolated Study): Retain WTMP for Station 41002 (N=518) to analyze sea-temperature coupling."],
             bg_rgb=(255, 250, 240), border_rgb=(240, 210, 160))

    # -------------------------------------------------------------
    # SLIDE 6: Exploratory Data Analysis & Empirical Coupling
    # -------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    create_slide_header(s6, "Exploratory Data Analysis: Key Physical Dynamics")
    # Embed Scatter Figure (WSPD vs GST & Missing WVHT)
    s6.shapes.add_picture(os.path.join("results", "03_eda", "03_scatter_wspd_wvht_gst.png"),
                          Inches(0.8), Inches(1.8), width=Inches(6.2))
    add_card(s6, Inches(7.3), Inches(1.8), Inches(5.2), Inches(5.0),
             "Observed Empirical Relationships",
             ["Near-Perfect Wind Coupling: Sustained wind speed (WSPD) and wind gust (GST) exhibit linear proportionality (r = +0.957; GST = 1.18 × WSPD + 0.58).",
              "Barometric Pressure Depressions: Weak negative correlation between BAR and WSPD (r = -0.198). Stormy wind peaks consistently align with barometric depressions (<1015 hPa).",
              "Seasonal Thermal Drift: Station 42040 air temperature climbs from 3.2°C in January to >30°C in June, capturing the North American continental seasonal cycle.",
              "WVHT Verification: Confirms zero data points available for significant wave height."])

    # -------------------------------------------------------------
    # SLIDE 7: Unsupervised k-Means Clustering
    # -------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    create_slide_header(s7, "Unsupervised k-Means Clustering: Model Selection")
    # Embed Silhouette / Elbow figure
    s7.shapes.add_picture(os.path.join("results", "04_clustering", "01_k_selection_silhouette_elbow.png"),
                          Inches(0.8), Inches(1.8), width=Inches(6.2))
    add_card(s7, Inches(7.3), Inches(1.8), Inches(5.2), Inches(5.0),
             "Cluster Evaluation & Standardization",
             ["Feature Standardization: Features (WSPD, GST, BAR, ATMP) standardized to Mean=0, Std=1, ensuring pressure (~1018 hPa) does not dominate wind (~5.9 m/s).",
              "Silhouette Score Evaluation (random_state=42):\n  • k = 2: 0.3537 (Optimal Global Silhouette)\n  • k = 3: 0.3338 (Secondary High Silhouette)\n  • k = 4: 0.2819 | k = 5: 0.2813 | k = 6: 0.2869",
              "Elbow Method: Within-cluster inertia drops sharply from k=2 (5,095) to k=3 (3,716), leveling off past k=4.",
              "Chosen Model: k=2 provides the most distinct, interpretable partition of marine atmospheric regimes."])

    # -------------------------------------------------------------
    # SLIDE 8: Cluster Profiling & Adjusted Rand Index Validation
    # -------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    create_slide_header(s8, "Cluster Profiles & Geographic Independence (ARI)")
    # Embed Cluster Scatter
    s8.shapes.add_picture(os.path.join("results", "04_clustering", "02_cluster_scatter_k2.png"),
                          Inches(0.8), Inches(1.8), width=Inches(6.2))
    add_card(s8, Inches(7.3), Inches(1.8), Inches(5.2), Inches(5.0),
             "Cluster Regimes & The ARI Test",
             ["Cluster 1 - Calm/Warm Regime (N=1,317, 67.09%):\n  • Wind Speed: 4.46 ± 1.72 m/s\n  • Pressure: 1018.59 ± 3.51 hPa\n  • Air Temp: 24.37 ± 3.82 °C",
              "Cluster 2 - Energetic/Cool Regime (N=646, 32.91%):\n  • Wind Speed: 8.91 ± 1.93 m/s (Gusts 11.36 m/s)\n  • Pressure: 1019.01 ± 6.23 hPa\n  • Air Temp: 19.40 ± 5.71 °C",
              "The Adjusted Rand Index (ARI) Test:\n  • ARI(Clusters, Station) = -0.0243\n  • Mathematical Proof: ARI near 0 proves clusters DO NOT recreate stations! Both buoys experience both weather states.",
              "Neutral Labeling: Described strictly by measurements, never as 'safe/dangerous' or 'PFZ'."])

    # -------------------------------------------------------------
    # SLIDE 9: Supervised Classification Formulation
    # -------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    create_slide_header(s9, "Supervised Classification: Problem Formulation")
    add_card(s9, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Target Formulation: Equal-Frequency Terciles",
             ["Physical Oceanographic Link: Wave height scales monotonically with wind energy (Hm0 ∝ U10^2). Wind speed terciles map 1-to-1 to sea-state energy terciles.",
              "Discretized Tercile Boundaries (N=1,963):\n  • Low Band: WSPD ≤ 4.60 m/s (N=654, 33.32%)\n  • Mid Band: 4.60 < WSPD ≤ 6.90 m/s (N=657, 33.47%)\n  • High Band: WSPD > 6.90 m/s (N=652, 33.21%)",
              "Balanced Classes: Perfectly balanced 3-class distribution.",
              "Majority-Class Baseline: Exactly 33.47% accuracy."])
    add_card(s9, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Predictor Quarantine & Evaluated Algorithms",
             ["Strict Feature Quarantine (Anti-Leakage):\n  • EXCLUDED: WSPD (Target Leakage)\n  • EXCLUDED: GST (Near-Leakage Gust Feature)\n  • EXCLUDED: Station ID & Coordinates (Location Shortcut)",
              "Active Predictors: Barometric Pressure (BAR) and Air Temperature (ATMP).",
              "Implemented Classifiers (Orange / Scikit-Learn):\n  1. Majority-Class Dummy Classifier (Baseline)\n  2. Decision Tree (max_depth=5, min_samples_leaf=20)\n  3. Random Forest (100 de-correlated trees)\n  4. Gaussian Naive Bayes (Probabilistic learner)"])

    # -------------------------------------------------------------
    # SLIDE 10: Model Benchmarking: 10-Fold CV vs. Chronological Split
    # -------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    create_slide_header(s10, "Model Benchmarking: Why Random CV is Optimistic")
    add_card(s10, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Stratified 10-Fold CV vs. Chronological Split",
             ["Stratified 10-Fold Cross-Validation:\n  • Majority Baseline: 33.47% Acc | 0.1672 Macro F1\n  • Decision Tree: 49.37% Acc | 0.4885 Macro F1\n  • Random Forest: 49.16% Acc | 0.4898 Macro F1\n  • Naive Bayes: 44.52% Acc | 0.4336 Macro F1",
              "Chronological Split (Train: Jan-Apr, Test: May-Jun):\n  • Majority Baseline: 24.03% Acc | 0.1292 Macro F1\n  • Decision Tree: 41.10% Acc | 0.3668 Macro F1\n  • Random Forest: 37.42% Acc | 0.3581 Macro F1\n  • Naive Bayes: 30.27% Acc | 0.2871 Macro F1",
              "Key Takeaway: All models clearly beat baseline, but chronological evaluation reveals real-world generalization."])
    add_card(s10, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "The Impact of Temporal Autocorrelation",
             ["Why is Random CV Optimistic (~49% vs ~37%)?\n  1. Synoptic Weather Persistence: Marine atmospheric systems evolve across 24 to 72 hours.",
              "2. Temporal Data Leakage: Random 10-fold CV scatters adjacent 3-hour readings from the SAME storm into both train and validation folds. The model 'peeks' at adjacent hours.",
              "3. Seasonal Shift: Training on winter/spring and testing on summer encounters calmer summer high-pressure ridges not seen in winter training.",
              "4. Spatial Inbalance: Station 41002 had only 29 training rows in April, but 489 testing rows in May-June!"],
             bg_rgb=(255, 250, 240), border_rgb=(240, 210, 160))

    # -------------------------------------------------------------
    # SLIDE 11: Honest Extra Experiments & Extracted Tree Rules
    # -------------------------------------------------------------
    s11 = prs.slides.add_slide(blank_layout)
    create_slide_header(s11, "Honest Extra Experiments & Interpretable Rules")
    add_card(s11, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Labelled Extra Experiments (Honest Reporting)",
             ["Exp (i) - Add DPD + APD (All-Null Sensors Imputed):\n  • 10-Fold CV: 49.31% (Delta = +0.15%)\n  • Chrono Split: 39.26% (Delta = +1.84%)\n  • Analysis: Zero variance constant features offer zero entropy reduction. Delta is random bootstrap noise.",
              "Exp (ii) - Add Station (Location Shortcut):\n  • 10-Fold CV: 51.20% (+2.04% boost)\n  • Chrono Split: 44.38% (+6.96% boost)\n  • Analysis: Confirms station acts as a spatial shortcut.",
              "Exp (iii) - Add GST (Near-Leakage Wind Gust):\n  • Accuracy surges to 92.87% (CV) and 92.84% (Chrono)!\n  • Analysis: Demonstrates catastrophic data leakage."])
    add_card(s11, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Extracted Decision Tree Rules (Jan-Apr Fit)",
             ["Physical Rule 1 (Cyclonic Depression):\n  IF BAR ≤ 1016.75 hPa\n  -> PREDICT High (Turbulent Marine Condition)\n  (Captures energetic cyclonic low-pressure systems).",
              "Physical Rule 2 (Warm Summer Anticyclone):\n  IF BAR > 1016.75 hPa AND ATMP > 24.25 °C\n  -> PREDICT Low (Calm Marine Condition)\n  (Captures tranquil warm high-pressure ridges).",
              "Physical Rule 3 (Transitional Conditions):\n  IF 1016.75 < BAR ≤ 1025.95 hPa AND 21.75 < ATMP ≤ 24.25 °C\n  -> PREDICT Mid (Moderate Marine Condition)."])

    # -------------------------------------------------------------
    # SLIDE 12: Limitations, Conclusion & Future Scope
    # -------------------------------------------------------------
    s12 = prs.slides.add_slide(blank_layout)
    create_slide_header(s12, "Limitations, Conclusion & Future Scope")
    add_card(s12, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Limitations & Responsible AI Disclaimer",
             ["US Marine Data Only: Buoys located in US Atlantic & Gulf of Mexico. Cannot generalize to Indian waters.",
              "Temporal Scope: 6-month observation window (Jan-Jun 2025) with extensive 116-day gap at Station 41002.",
              "Absent Wave Sensors: Accelerometer wave payloads unrecorded (0 valid WVHT rows).",
              "Ethical Safeguard: Derived tercile labels are statistical research bands, NEVER operational sea-state or safety advisories. Models must NOT be used for navigation."])
    add_card(s12, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Conclusion & Future Scope (SIH Platform)",
             ["Conclusions:\n  • Data mining discovers cross-station atmospheric regimes (k=2, ARI=-0.0243).\n  • Surface pressure and temperature predict marine conditions above baseline (49.4% vs 33.5%).\n  • Chronological validation is mandatory to prevent temporal autocorrelation leakage.",
              "Future Scope (SIH26176 Alignment):\n  • Task B: Satellite SST + Chlorophyll-a fusion for Potential Fishing Zone (PFZ) advisory prediction (INCOIS methodology).\n  • Agentic AI: Multi-agent routing, automated coastal SMS alerts, and conversational assistants."],
             bg_rgb=(245, 252, 245), border_rgb=(180, 220, 180))

    out_pptx_path = "Presentation.pptx"
    prs.save(out_pptx_path)
    print(f"Presentation.pptx successfully created and saved to {out_pptx_path}!")

if __name__ == "__main__":
    generate_presentation()
