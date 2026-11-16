import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_header_styled(doc, text, level):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.space_before = Pt(12)
    h.paragraph_format.space_after = Pt(4)
    h.paragraph_format.keep_with_next = True
    for run in h.runs:
        run.font.name = 'Arial'
        if level == 1:
            run.font.size = Pt(16)
            run.font.bold = True
            run.font.color.rgb = RGBColor(16, 44, 87) # Deep Navy
        elif level == 2:
            run.font.size = Pt(13)
            run.font.bold = True
            run.font.color.rgb = RGBColor(40, 80, 130)
        elif level == 3:
            run.font.size = Pt(11)
            run.font.bold = True
            run.font.color.rgb = RGBColor(60, 60, 60)
    return h

def add_callout(doc, text, title="ACADEMIC HONESTY & SCOPE NOTICE", border_color="003366", bg_color="F0F4F8"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)

    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}>'
                        f'<w:top w:val="none"/>'
                        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/>'
                        f'<w:bottom w:val="none"/>'
                        f'<w:right w:val="none"/>'
                        f'</w:tcBorders>')
    tcPr.append(borders)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    r_title = p.add_run(f"[{title}]\n")
    r_title.bold = True
    r_title.font.name = 'Arial'
    r_title.font.size = Pt(10)
    r_title.font.color.rgb = RGBColor(0, 51, 102)

    r_text = p.add_run(text)
    r_text.font.name = 'Arial'
    r_text.font.size = Pt(9.5)
    r_text.font.color.rgb = RGBColor(40, 40, 40)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def format_table(table, header_bg="1A365D", alt_bg="F7FAFC"):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, row in enumerate(table.rows):
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        if i == 0:
            trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))

        for cell in row.cells:
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            if i == 0:
                set_cell_background(cell, header_bg)
                for p in cell.paragraphs:
                    p.paragraph_format.space_before = Pt(2)
                    p.paragraph_format.space_after = Pt(2)
                    for run in p.runs:
                        run.font.name = 'Arial'
                        run.font.size = Pt(9)
                        run.font.bold = True
                        run.font.color.rgb = RGBColor(255, 255, 255)
            else:
                if i % 2 == 1:
                    set_cell_background(cell, "FFFFFF")
                else:
                    set_cell_background(cell, alt_bg)
                for p in cell.paragraphs:
                    p.paragraph_format.space_before = Pt(2)
                    p.paragraph_format.space_after = Pt(2)
                    for run in p.runs:
                        run.font.name = 'Arial'
                        run.font.size = Pt(8.5)
                        run.font.color.rgb = RGBColor(30, 30, 30)

def generate_report():
    doc = Document()

    # Set 1-inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # -------------------------------------------------------------
    # TITLE & METADATA
    # -------------------------------------------------------------
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(10)
    title_p.paragraph_format.space_after = Pt(4)
    title_p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = title_p.add_run("Marine Condition Analysis and Classification\nUsing Data Mining")
    r_title.bold = True
    r_title.font.name = 'Arial'
    r_title.font.size = Pt(20)
    r_title.font.color.rgb = RGBColor(16, 44, 87)

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(16)
    sub_p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = sub_p.add_run("An Empirical Exploration of NDBC In-Situ Buoy Meteorological Observations (CRISP-DM Framework)\n"
                          "Third-Year B.Tech Data Mining Project Report | October 2026")
    r_sub.font.name = 'Arial'
    r_sub.font.size = Pt(10.5)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(80, 80, 80)

    # Notice banner
    add_callout(doc,
                "1. DATASET GEOGRAPHY: All data analyzed originates from United States marine waters (NOAA National Data Buoy Center) in the Atlantic Ocean and the Gulf of Mexico. This project DOES NOT contain Indian waters data.\n"
                "2. NO INVENTED NUMBERS: Every quantitative metric, table, figure, and rule was computed by directly running Python and Orange 3 scripts on the raw observational CSV.\n"
                "3. DERIVED RESEARCH LABELS: Cluster groupings and wind-wave terciles represent unsupervised clusters and sample percentiles of this specific sample, NOT official maritime safety categories or operational navigation advisories.\n"
                "4. PROJECT SCOPE: Inspired by Smart India Hackathon (SIH26176) concepts. Chatbots, agentic pipelines, route optimization, and Potential Fishing Zone (PFZ) advisory prediction are formally categorized under Future Scope only.",
                title="MANDATORY ACADEMIC AND ETHICAL COMPLIANCE STATEMENT", border_color="C53030", bg_color="FFF5F5")

    # -------------------------------------------------------------
    # 1. ABSTRACT
    # -------------------------------------------------------------
    add_header_styled(doc, "1. Abstract", level=1)
    p = doc.add_paragraph(
        "Modern marine intelligence platforms require robust analytical pipelines to decipher continuous oceanographic "
        "and meteorological telemetry. This project investigates whether standard data mining techniques—specifically "
        "k-Means unsupervised clustering, Decision Trees, Random Forests, and Gaussian Naive Bayes—can discover meaningful "
        "atmospheric-marine patterns and classify observed conditions from in-situ buoy telemetry. Working with real-world 3-hourly "
        "standard meteorological observations from NOAA National Data Buoy Center (NDBC) ERDDAP dataset cwwcNDBCMet covering January to "
        "June 2025 (1,967 rows across two US marine stations), this study resolves real-world sensor non-reporting challenges, evaluates "
        "rigorous preprocessing thresholds, and benchmark predictive performance. An optimal clustering model at k=2 (Silhouette coefficient = 0.3537) "
        "reveals distinct marine meteorological regimes (a calm warm regime comprising 67.09% of records and an energetic cool regime comprising 32.91%) "
        "with an Adjusted Rand Index against buoy station of -0.0243, confirming that clusters capture shared physical weather states rather than "
        "geographic location. In supervised classification of marine condition terciles using atmospheric pressure and air temperature, "
        "the Decision Tree (49.37% CV accuracy) and Random Forest (49.16% CV accuracy) substantially outperform the 33.47% majority baseline. "
        "Crucially, evaluating models under a chronological split (Jan-Apr training vs. May-Jun testing) reveals a drop to 41.10% and 37.42% accuracy, "
        "empirically demonstrating how temporal autocorrelation inflates standard random cross-validation. These findings underscore the "
        "imperative of rigorous validation in operational marine data mining."
    )
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # 2. INTRODUCTION & PROBLEM STATEMENT
    # -------------------------------------------------------------
    add_header_styled(doc, "2. Introduction and Problem Statement", level=1)
    doc.add_paragraph(
        "Autonomous marine surveillance, commercial maritime routing, and coastal community safety depend fundamentally on "
        "reliable marine condition situational awareness. While satellite remote sensing provides broad spatial coverage, "
        "in-situ moored buoys deployed by agencies like the National Oceanic and Atmospheric Administration (NOAA) National Data "
        "Buoy Center (NDBC) supply the continuous ground truth across surface wind speed, barometric pressure, air temperature, "
        "and sea surface temperature. However, raw marine telemetry is characterized by sensor outages, extreme environmental degradation, "
        "missing records, and high temporal dependency."
    )
    doc.add_paragraph(
        "The primary research question addressed in this study is:\n"
        "Can data mining discover meaningful patterns in marine and meteorological observations and accurately classify observed conditions "
        "using surface atmospheric predictors without location shortcuts or data leakage?"
    )

    # -------------------------------------------------------------
    # 3. OBJECTIVES & SCOPE
    # -------------------------------------------------------------
    add_header_styled(doc, "3. Objectives and Scope Definition", level=1)
    doc.add_paragraph(
        "The specific technical objectives of this project include:\n"
        "1. Perform comprehensive forensic data inspection on NOAA NDBC buoy data, auditing missingness rates, time spans, and station deficits.\n"
        "2. Formulate evidence-based preprocessing and plausibility screening rules to clean telemetry without distorting spatial diversity.\n"
        "3. Conduct exploratory data analysis to evaluate wind-gust coupling, barometric depressions, and thermal dynamics.\n"
        "4. Discover unsupervised marine meteorological regimes using k-Means clustering and validate cluster independence against station geography using the Adjusted Rand Index.\n"
        "5. Benchmark multi-class supervised classification algorithms under both stratified cross-validation and a temporal chronological split, explaining the effect of temporal autocorrelation.\n"
        "6. Conduct honest extra experiments evaluating zero-variance sensor imputation, location shortcuts, and near-leakage features."
    )
    doc.add_paragraph(
        "Scope Boundaries: This investigation is inspired by concepts in Smart India Hackathon problem statement SIH26176 (Agentic-AI Marine "
        "Intelligence Platform). To guarantee academic feasibility and rigorous execution within a B.Tech Data Mining curriculum, "
        "the project deliberately focuses strictly on the data mining and machine learning modeling core. Conversational agents, multi-agent "
        "orchestration, automated emergency SMS alerts, dynamic vessel routing, and satellite-derived Potential Fishing Zone (PFZ) advisory "
        "generation are formally demarcated as Future Scope."
    )

    # -------------------------------------------------------------
    # 4. DATASET DESCRIPTION & THE 1,967 VS ~4,300 ROW GAP
    # -------------------------------------------------------------
    add_header_styled(doc, "4. Dataset Description & Discrepancy Investigation", level=1)
    doc.add_paragraph(
        "The raw dataset analyzed is sourced from the NOAA National Data Buoy Center (NDBC) Standard Meteorological Buoy Data via the NOAA "
        "CoastWatch ERDDAP server (Dataset ID: cwwcNDBCMet). The data represents 3-hourly observations downloaded for the 6-month period "
        "from January 1, 2025 to June 30, 2025. All observations originate entirely from United States territorial marine waters."
    )

    add_header_styled(doc, "4.1 Forensic Investigation: Row Count Gap (1,967 vs. Expected ~4,300 Rows)", level=2)
    doc.add_paragraph(
        "An initial theoretical calculation for 3 buoy stations over a 6-month period (181 calendar days) with 3-hourly sampling (8 readings per day) "
        "yields 1,448 expected records per station, or 4,344 total records across 3 stations. When loaded into Orange Data Mining, the dataset "
        "contained exactly 1,967 rows—a deficit of 2,377 rows. Forensic inspection revealed two distinct root causes:\n"
        "1. Station Omission: The downloaded file contained only TWO stations: Station 42040 and Station 41002. An intended 3rd station was completely omitted from the query.\n"
        "2. Station 41002 Temporal Truncation: While Station 42040 (Luke Offshore Test Platform, Gulf of Mexico) covered the entire 181-day span (1,449 rows, matching theoretical expectations), "
        "Station 41002 (South Hatteras, Atlantic Ocean) only reported data from April 27, 2025 to June 30, 2025 (518 rows, covering only 64.6 days). Over 116 days of winter and early spring data "
        "were unrecorded, accounting for a deficit of ~930 records."
    )

    add_header_styled(doc, "4.2 Mathematical Reconciliation of Orange's '34% Missing Values' Diagnostic", level=2)
    doc.add_paragraph(
        "Orange Data Mining reported an overall missingness rate of ~34% upon loading raw.csv. This diagnostic reflects Orange's internal feature domain "
        "architecture: Orange treats the 11 numeric attributes as the feature domain X (treating 'time (UTC)' as metadata). The domain thus consists of "
        "1,967 × 11 = 21,637 total feature cells. The actual missing cells across X are:\n"
        "• WVHT (m), DPD (s), APD (s): 1,967 missing each (100.0% unrecorded; wave sensors unmounted or offline)\n"
        "• WTMP (degree_C): 1,449 missing (73.67% overall; completely absent at Station 42040)\n"
        "• WSPD, GST, BAR, ATMP: 2 missing cells each (0.10%, occurring across 4 distinct records at Station 42040)\n"
        "Summing these yields exactly 7,358 missing cells out of 21,637 cells, resulting in 34.0066% (exactly 34.01%), fully reconciling Orange's diagnostic."
    )

    # -------------------------------------------------------------
    # 5. PREPROCESSING & CLEANING METHODOLOGY
    # -------------------------------------------------------------
    add_header_styled(doc, "5. Data Preprocessing and Cleaning Methodology", level=1)
    doc.add_paragraph(
        "Preprocessing decisions were established using rigorous empirical criteria documented in DECISIONS.md:\n"
        "1. Missingness Threshold (50.0% Rule): Attributes with >50% missingness were dropped. WVHT, DPD, and APD (100% missing) were dropped universally.\n"
        "2. Geographic Preservation vs. WTMP: Water temperature (WTMP) has 73.67% missingness overall. Requiring complete cases on WTMP drops 100% of Station 42040 (1,449 rows), "
        "collapsing the dataset into a single-buoy Atlantic sample. To preserve multi-station diversity, the primary core pipeline retains WSPD, GST, BAR, and ATMP, "
        "while WTMP is investigated in an isolated Atlantic subset (N=518).\n"
        "3. Analyst Plausibility Bounds: Non-official heuristic screening boundaries were verified: WSPD [0, 50] m/s, GST [0, 70] m/s, BAR [900, 1100] hPa, ATMP [-40, 50] °C, WTMP [-2, 40] °C. "
        "Zero records violated these bounds.\n"
        "4. Final Sample Accounting: In the core pipeline, 1,963 clean rows were retained (99.80%), with only 4 records dropped due to intermittent sensor dropouts at Station 42040."
    )

    # Table of cleaning accounting
    tbl_clean = doc.add_table(rows=5, cols=6)
    clean_data = [
        ["Pipeline", "Station", "Raw Rows", "Kept Rows", "Dropped", "Retention Rate"],
        ["Core Pipeline", "All Stations", "1,967", "1,963", "4", "99.80%"],
        ["Core Pipeline", "Station 42040 (Gulf)", "1,449", "1,445", "4", "99.72%"],
        ["Core Pipeline", "Station 41002 (Atlantic)", "518", "518", "0", "100.00%"],
        ["WTMP Pipeline", "All Stations", "1,967", "518", "1,449", "26.33%"]
    ]
    for r_idx, row in enumerate(clean_data):
        for c_idx, val in enumerate(row):
            tbl_clean.cell(r_idx, c_idx).text = val
    format_table(tbl_clean)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # -------------------------------------------------------------
    # 6. EXPLORATORY DATA ANALYSIS (EDA)
    # -------------------------------------------------------------
    add_header_styled(doc, "6. Exploratory Data Analysis (EDA)", level=1)
    doc.add_paragraph(
        "Exploratory analysis established baseline distributions, cross-station variations, and atmospheric coupling. "
        "Figure 1 displays the distributions of core meteorological variables, highlighting right-skewed wind speeds (mean 5.92 m/s, max 15.30 m/s) "
        "and Gaussian-like barometric pressure (mean 1018.73 hPa, std 4.59 hPa)."
    )

    # Embed Figure 1: Histograms
    p_img1 = doc.add_paragraph()
    p_img1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img1.paragraph_format.space_after = Pt(2)
    doc.add_picture(os.path.join("results", "03_eda", "01_histograms_core_features.png"), width=Inches(5.8))
    cap1 = doc.add_paragraph("Figure 1: Histograms and Kernel Density Estimates for Core Buoy Meteorological Features (N=1,963).")
    cap1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap1.runs[0].font.size = Pt(8.5); cap1.runs[0].font.italic = True

    doc.add_paragraph(
        "Figure 2 illustrates comparative box plots across both marine stations. Station 42040 (Gulf of Mexico) displays a much wider air temperature range "
        "(3.2°C to 30.9°C) reflecting winter-to-summer continental air mass movements, whereas Station 41002 (Atlantic Ocean, observed only from late April) "
        "is confined to warm late-spring conditions (mean 23.36°C)."
    )

    # Embed Figure 2: Boxplots
    doc.add_picture(os.path.join("results", "03_eda", "02_boxplots_by_station.png"), width=Inches(5.8))
    cap2 = doc.add_paragraph("Figure 2: Distributional Comparison of Core Features Between Buoy Stations.")
    cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap2.runs[0].font.size = Pt(8.5); cap2.runs[0].font.italic = True

    doc.add_paragraph(
        "Figure 3 presents the bivariate relationships. The left panel verifies that Significant Wave Height (WVHT) contains zero observations across "
        "both buoys. The right panel demonstrates near-perfect linear coupling between sustained wind speed (WSPD) and wind gust (GST), with a Pearson "
        "correlation coefficient of r = +0.957 (GST = 1.18 × WSPD + 0.58). Figure 4 and Figure 5 depict the multi-feature correlation matrices and "
        "the 6-month continuous time series profiles."
    )

    # Embed Figure 3 & Figure 4
    doc.add_picture(os.path.join("results", "03_eda", "03_scatter_wspd_wvht_gst.png"), width=Inches(5.8))
    cap3 = doc.add_paragraph("Figure 3: Scatter Plot of WSPD vs. Missing WVHT (Left) and WSPD vs. GST with Regression Fit (Right).")
    cap3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap3.runs[0].font.size = Pt(8.5); cap3.runs[0].font.italic = True

    doc.add_picture(os.path.join("results", "03_eda", "04_correlation_matrix.png"), width=Inches(5.8))
    cap4 = doc.add_paragraph("Figure 4: Pearson Correlation Matrices for Core Variables (Left) and SST Subset (Right).")
    cap4.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap4.runs[0].font.size = Pt(8.5); cap4.runs[0].font.italic = True

    # -------------------------------------------------------------
    # 7. ALGORITHMIC FRAMEWORK
    # -------------------------------------------------------------
    add_header_styled(doc, "7. Algorithmic Foundations", level=1)
    doc.add_paragraph(
        "To satisfy curriculum objectives, four core data mining algorithms were implemented and parameterized:\n"
        "• k-Means Clustering: An unsupervised partitioning algorithm that minimizes within-cluster sum of squares (inertia). Features were standardized (mean=0, std=1) to prevent pressure (magnitude ~1018) from overwhelming wind speed (magnitude ~5.9). Centroid updates follow Euclidean distance minimization.\n"
        "• Decision Tree Classifier: A non-parametric supervised learner utilizing recursive binary partitioning. Splits are selected to maximize Gini impurity reduction. To avoid overfitting on 3-hourly data, maximum tree depth was constrained to 5 and minimum leaf samples to 20.\n"
        "• Random Forest Classifier: An ensemble method constructing 100 de-correlated decision trees trained via bootstrap aggregating (bagging) with random feature subspace selection, mitigating individual tree variance.\n"
        "• Gaussian Naive Bayes: A probabilistic classifier grounded in Bayes' Theorem assuming class-conditional feature independence following normal distributions: P(y|X) ∝ P(y) ∏ P(x_i|y)."
    )

    # -------------------------------------------------------------
    # 8. K-MEANS CLUSTERING RESULTS & EVALUATION
    # -------------------------------------------------------------
    add_header_styled(doc, "8. k-Means Clustering Results and Discussion", level=1)
    doc.add_paragraph(
        "Standardized features (WSPD, GST, BAR, ATMP) were partitioned across k = 2 to 6 with fixed random_state=42. "
        "Silhouette analysis (Figure 6, left) identified k=2 as the mathematical optimum with a silhouette score of 0.3537 (inertia = 5095.42), "
        "followed closely by k=3 (silhouette = 0.3338, inertia = 3716.41). k=4, 5, and 6 yielded lower silhouette coefficients (<0.29)."
    )

    # Embed Figure 6 & 7 (Clustering)
    doc.add_picture(os.path.join("results", "04_clustering", "01_k_selection_silhouette_elbow.png"), width=Inches(5.8))
    cap6 = doc.add_paragraph("Figure 5: Cluster Evaluation: Silhouette Scores and Within-Cluster Inertia across k=2 to 6.")
    cap6.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap6.runs[0].font.size = Pt(8.5); cap6.runs[0].font.italic = True

    doc.add_picture(os.path.join("results", "04_clustering", "02_cluster_scatter_k2.png"), width=Inches(5.8))
    cap7 = doc.add_paragraph("Figure 6: k-Means (k=2) Cluster Scatter Plots with Centroids (X).")
    cap7.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap7.runs[0].font.size = Pt(8.5); cap7.runs[0].font.italic = True

    add_header_styled(doc, "8.1 Cluster Profiling and Neutral Characterization", level=2)
    doc.add_paragraph(
        "Cluster profiles in physical units are summarized below (adhering strictly to neutral measured descriptors):\n"
        "• Cluster 1 (Calm/Warm Moderate Regime, N=1,317, 67.09%): Characterized by mean wind speed of 4.46 ± 1.72 m/s, wind gusts of 5.70 ± 1.92 m/s, barometric pressure of 1018.59 ± 3.51 hPa, and air temperature of 24.37 ± 3.82 °C.\n"
        "• Cluster 2 (Energetic/Cool Disturbed Regime, N=646, 32.91%): Characterized by mean wind speed of 8.91 ± 1.93 m/s, wind gusts of 11.36 ± 2.45 m/s, barometric pressure of 1019.01 ± 6.23 hPa, and air temperature of 19.40 ± 5.71 °C."
    )

    add_header_styled(doc, "8.2 Adjusted Rand Index (ARI) Validation", level=2)
    doc.add_paragraph(
        "A critical danger in multi-station clustering is that algorithms merely learn geographic buoy coordinates. Cross-tabulation revealed "
        "Cluster 1 contains 401 records from Station 41002 and 916 records from Station 42040. Cluster 2 contains 117 records from Station 41002 "
        "and 529 records from Station 42040. Computing the Adjusted Rand Index (ARI) between cluster labels and buoy station yielded:\n"
        "ARI(Clusters, Station) = -0.0243\n"
        "An ARI value near zero statistically confirms that cluster assignments are independent of station identity. The clusters capture genuine "
        "cross-station atmospheric regimes rather than geographic buoy identity."
    )

    # -------------------------------------------------------------
    # 9. SUPERVISED CLASSIFICATION BENCHMARK
    # -------------------------------------------------------------
    add_header_styled(doc, "9. Supervised Classification Results and Discussion", level=1)
    doc.add_paragraph(
        "Target Formulation: In physical oceanography, significant wave height and sea-state energy scale monotonically with surface wind speed "
        "(Pierson-Moskowitz / SMB empirical models: Hm0 ∝ U10^2). Discretising wind speed into 3 equal-frequency terciles (Low: ≤ 4.60 m/s; "
        "Mid: 4.60 to 6.90 m/s; High: > 6.90 m/s) establishes a perfectly balanced 3-class target (Low: 654, Mid: 657, High: 652 records). "
        "The majority-class baseline is exactly 33.47%."
    )
    doc.add_paragraph(
        "Predictors: To prevent target leakage, WSPD is excluded. Wind gust (GST) is excluded as near-leakage. Station ID and coordinates are "
        "excluded as location shortcuts. Classifiers rely solely on barometric pressure (BAR) and air temperature (ATMP)."
    )

    # Table of Classification Metrics
    add_header_styled(doc, "9.1 Comparative Performance: 10-Fold CV vs. Chronological Split", level=2)
    tbl_class = doc.add_table(rows=9, cols=7)
    class_headers = ["Model", "Evaluation Protocol", "Accuracy", "Macro Prec", "Macro Rec", "Macro F1", "F1 (Low/Mid/High)"]
    class_rows = [
        class_headers,
        ["Majority Baseline", "Stratified 10-Fold CV", "33.47%", "0.1116", "0.3333", "0.1672", "0.00 / 0.50 / 0.00"],
        ["Decision Tree", "Stratified 10-Fold CV", "49.37%", "0.5195", "0.4940", "0.4885", "0.47 / 0.47 / 0.53"],
        ["Random Forest", "Stratified 10-Fold CV", "49.16%", "0.4922", "0.4920", "0.4898", "0.50 / 0.42 / 0.54"],
        ["Naive Bayes", "Stratified 10-Fold CV", "44.52%", "0.4553", "0.4457", "0.4336", "0.51 / 0.29 / 0.50"],
        ["Majority Baseline", "Chrono (Jan-Apr / May-Jun)", "24.03%", "0.0801", "0.3333", "0.1292", "0.00 / 0.00 / 0.39"],
        ["Decision Tree", "Chrono (Jan-Apr / May-Jun)", "41.10%", "0.3861", "0.4325", "0.3668", "0.55 / 0.12 / 0.43"],
        ["Random Forest", "Chrono (Jan-Apr / May-Jun)", "37.42%", "0.3707", "0.4061", "0.3581", "0.46 / 0.19 / 0.42"],
        ["Naive Bayes", "Chrono (Jan-Apr / May-Jun)", "30.27%", "0.3361", "0.3372", "0.2871", "0.15 / 0.38 / 0.33"]
    ]
    for r_idx, row in enumerate(class_rows):
        for c_idx, val in enumerate(row):
            tbl_class.cell(r_idx, c_idx).text = val
    format_table(tbl_class)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # Embed Figure 8: Confusion Matrices
    doc.add_picture(os.path.join("results", "05_classification", "01_confusion_matrices.png"), width=Inches(6.2))
    cap8 = doc.add_paragraph("Figure 7: Confusion Matrices for Stratified 10-Fold Cross-Validation (Top) and Chronological Split (Bottom).")
    cap8.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap8.runs[0].font.size = Pt(8.5); cap8.runs[0].font.italic = True

    add_header_styled(doc, "9.2 Discussion: Why Random CV is Overly Optimistic", level=2)
    doc.add_paragraph(
        "A cornerstone finding of this research is the empirical performance degradation between 10-fold cross-validation and chronological splitting. "
        "Under 10-fold CV, Decision Tree and Random Forest achieve ~49.4% and ~49.2% accuracy. Under the chronological split (training on Jan-Apr, testing on May-Jun), "
        "accuracy declines sharply to 41.10% and 37.42%.\n"
        "Root Cause: Marine atmospheric systems exhibit strong temporal autocorrelation. Weather phenomena (such as frontal depressions or high-pressure ridges) "
        "persist across synoptic time scales of 24 to 72 hours. In random k-fold cross-validation, consecutive 3-hourly observations from the exact same weather event "
        "are randomly scattered into both training and validation folds. The classifier effectively 'peeks' at adjacent hours, inflating validation metrics. "
        "In contrast, the chronological split tests real forward temporal generalization across seasonal transitions (winter/spring into summer), providing an "
        "authentic assessment of real-world operational predictive power."
    )

    add_header_styled(doc, "9.3 Extracted Decision Tree Rules", level=2)
    doc.add_paragraph(
        "The Decision Tree trained on the Jan-Apr historical baseline extracted physically meaningful meteorological rules:\n"
        "• Storm/Depression Rule: When Barometric Pressure ≤ 1016.75 hPa, the model consistently predicts class 'High' (turbulent wind energy), reflecting cyclonic low-pressure dynamics.\n"
        "• Summer Anticyclone Rule: When Barometric Pressure > 1016.75 hPa and Air Temperature > 24.25 °C, the model predicts class 'Low' (calm marine conditions), capturing calm warm high-pressure ridges.\n"
        "• Intermediate Transition Rule: For moderate pressure (1016.75 < BAR ≤ 1025.95 hPa) and moderate temperature (21.75 < ATMP ≤ 24.25 °C), the model assigns class 'Mid'."
    )

    # Table of Extra Experiments
    add_header_styled(doc, "9.4 Labelled Extra Experiments (Honest Empirical Reporting)", level=2)
    tbl_extra = doc.add_table(rows=5, cols=5)
    extra_data = [
        ["Experiment Suite", "10-Fold CV Acc", "10-Fold F1", "Chrono Acc", "Chrono F1"],
        ["Baseline Features (BAR, ATMP)", "49.16%", "0.4898", "37.42%", "0.3581"],
        ["(i) Add DPD + APD (Null Sensors Imputed)", "49.31%", "0.4926", "39.26%", "0.3710"],
        ["(ii) Add Station (Location Shortcut)", "51.20%", "0.5113", "44.38%", "0.4400"],
        ["(iii) Add GST (Near-Leakage Feature)", "92.87%", "0.9287", "92.84%", "0.9284"]
    ]
    for r_idx, row in enumerate(extra_data):
        for c_idx, val in enumerate(row):
            tbl_extra.cell(r_idx, c_idx).text = val
    format_table(tbl_extra)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    doc.add_paragraph(
        "Analysis of Extra Experiments:\n"
        "• Exp (i) - Null Sensors: DPD and APD are 100% missing. Imputing zero variance yields a negligible delta (+0.15% CV) attributable solely to random forest bootstrap variance.\n"
        "• Exp (ii) - Station Shortcut: Adding station boosts accuracy by +2.04% (CV) and +6.96% (Chrono). Buoy identity acts as a geographic shortcut memorizing localized climatology.\n"
        "• Exp (iii) - Near-Leakage (GST): Adding wind gust causes accuracy to surge to 92.87%, proving that including concurrent gust measurements constitutes target leakage."
    )

    # -------------------------------------------------------------
    # 10. LIMITATIONS & ETHICAL SAFEGUARDS
    # -------------------------------------------------------------
    add_header_styled(doc, "10. Limitations and Ethical Safeguards", level=1)
    doc.add_paragraph(
        "Academic honesty requires candid disclosure of study constraints:\n"
        "1. Geographic Domain: Observations originate exclusively from United States coastal waters (Atlantic and Gulf of Mexico). They cannot be generalized to the Arabian Sea or Bay of Bengal.\n"
        "2. Temporal Scope: The dataset covers only 6 months (January to June 2025), precluding multi-year climatological analysis.\n"
        "3. Station Attrition: Only 2 stations were captured rather than the planned 3, and Station 41002 experienced an extensive 116-day gap.\n"
        "4. Derived Tercile Labels: Target categories represent statistical sample percentiles, not statutory navigation thresholds or WMO sea-state codes.\n"
        "5. Sensor Failure: Accelerometer-based wave height sensors were entirely absent (100% unrecorded).\n"
        "6. Operational Disclaimer: Models must NEVER be utilized for navigational routing, life-safety operations, or commercial fisheries management."
    )

    # -------------------------------------------------------------
    # 11. CONCLUSION & FUTURE SCOPE
    # -------------------------------------------------------------
    add_header_styled(doc, "11. Conclusion and Future Scope", level=1)
    doc.add_paragraph(
        "Conclusion: This project successfully deployed end-to-end data mining to analyze marine and meteorological buoy telemetry. "
        "k-Means clustering uncovered genuine physical atmospheric regimes (ARI = -0.0243 vs. station). Supervised models demonstrated "
        "that barometric pressure and temperature can predict marine conditions significantly above baseline, while chronological evaluation "
        "exposed the optimism of standard cross-validation caused by temporal autocorrelation."
    )
    doc.add_paragraph(
        "Future Scope (SIH Platform Alignment):\n"
        "• Task B: Fusion of satellite Sea Surface Temperature (SST) and Chlorophyll-a telemetry to predict Potential Fishing Zones (PFZs), integrating INCOIS advisory methodologies.\n"
        "• Agentic Architecture: Integrating autonomous multi-agent reasoning, automated weather routing, and conversational interfaces for coastal communities.\n"
        "• High-Frequency Telemetry: Incorporating 10-minute real-time NDBC feeds and deploying LSTM/Transformer temporal deep learning models."
    )

    # -------------------------------------------------------------
    # 12. VERIFIED REFERENCES
    # -------------------------------------------------------------
    add_header_styled(doc, "12. References (Strictly Verified)", level=1)
    refs = [
        "1. NOAA CoastWatch / ERDDAP. (2025). NDBC Standard Meteorological Buoy Data (Dataset ID: cwwcNDBCMet). National Oceanic and Atmospheric Administration. https://coastwatch.pfeg.noaa.gov/erddap/tabledap/cwwcNDBCMet.html",
        "2. NOAA National Data Buoy Center (NDBC). (2025). Measurement Descriptions and Instrumentation Specifications. National Oceanic and Atmospheric Administration. https://www.ndbc.noaa.gov/measdes.shtml",
        "3. Indian National Centre for Ocean Information Services (INCOIS). (2025). Potential Fishing Zone (PFZ) Advisory Mission & Methodology. Ministry of Earth Sciences, Government of India. https://incois.gov.in/MarineFisheries/PfzAdvisory",
        "4. Demšar, J., Curk, T., Erjavec, A., Gorup, Č., Hočevar, T., Milutinovič, M., Možina, M., Polajnar, M., Toplak, M., Starič, A., Štajdohar, M., Umek, L., Žagar, L., Žbontar, J., Žitnik, M., & Zupan, B. (2013). Orange: Data Mining Toolbox in Python. Journal of Machine Learning Research, 14(1), 2349-2353. https://orangedatamining.com/docs/"
    ]
    for r in refs:
        p_ref = doc.add_paragraph(r)
        p_ref.paragraph_format.left_indent = Inches(0.4)
        p_ref.paragraph_format.space_after = Pt(4)
        p_ref.runs[0].font.size = Pt(9)

    out_docx_path = "Report.docx"
    doc.save(out_docx_path)
    print(f"Report.docx successfully created and saved to {out_docx_path}!")

if __name__ == "__main__":
    generate_report()
