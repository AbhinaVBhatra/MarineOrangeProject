import os
import sys
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
    h.paragraph_format.space_before = Pt(14)
    h.paragraph_format.space_after = Pt(4)
    h.paragraph_format.keep_with_next = True
    for run in h.runs:
        run.font.name = 'Times New Roman'
        if level == 1:
            run.font.size = Pt(14)
            run.font.bold = True
            run.font.color.rgb = RGBColor(16, 44, 87) # Deep Navy
        elif level == 2:
            run.font.size = Pt(12)
            run.font.bold = True
            run.font.color.rgb = RGBColor(35, 75, 125)
        elif level == 3:
            run.font.size = Pt(10.5)
            run.font.bold = True
            run.font.italic = True
            run.font.color.rgb = RGBColor(50, 50, 50)
    return h

def add_body_p(doc, text, space_after=6, bold_prefix=None):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Times New Roman'
        r_pre.font.size = Pt(10.5)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(20, 20, 20)
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(10.5)
    r.font.color.rgb = RGBColor(30, 30, 30)
    return p

def add_callout(doc, text, title="ACADEMIC HONESTY & ETHICAL COMPLIANCE", border_color="003366", bg_color="F4F6F9"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)

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
    p.paragraph_format.line_spacing = 1.1
    r_title = p.add_run(f"[{title}]\n")
    r_title.bold = True
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(9.5)
    r_title.font.color.rgb = RGBColor(0, 51, 102)

    r_text = p.add_run(text)
    r_text.font.name = 'Times New Roman'
    r_text.font.size = Pt(9.0)
    r_text.font.color.rgb = RGBColor(40, 40, 40)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def format_table(table, header_bg="162C57", alt_bg="F8FAFC"):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, row in enumerate(table.rows):
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        if i == 0:
            trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))

        for cell in row.cells:
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            set_cell_margins(cell, top=70, bottom=70, left=100, right=100)
            if i == 0:
                set_cell_background(cell, header_bg)
                for p in cell.paragraphs:
                    p.paragraph_format.space_before = Pt(2)
                    p.paragraph_format.space_after = Pt(2)
                    for run in p.runs:
                        run.font.name = 'Times New Roman'
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
                        run.font.name = 'Times New Roman'
                        run.font.size = Pt(8.5)
                        run.font.color.rgb = RGBColor(30, 30, 30)

def add_figure_with_caption(doc, img_path, caption_text, width=Inches(5.8)):
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(8)
    p_img.paragraph_format.space_after = Pt(2)
    doc.add_picture(img_path, width=width)
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(10)
    r_cap = p_cap.add_run(caption_text)
    r_cap.font.name = 'Times New Roman'
    r_cap.font.size = Pt(8.5)
    r_cap.font.italic = True
    r_cap.font.color.rgb = RGBColor(60, 60, 60)

def build_paper():
    doc = Document()

    # Configure 1.0 inch margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # -------------------------------------------------------------
    # TITLE & METADATA
    # -------------------------------------------------------------
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(12)
    title_p.paragraph_format.space_after = Pt(6)
    title_p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = title_p.add_run("Marine Condition Analysis and Classification\nUsing Data Mining")
    r_title.bold = True
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(20)
    r_title.font.color.rgb = RGBColor(16, 44, 87)

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(18)
    sub_p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = sub_p.add_run("An Empirical Investigation of In-Situ Meteorological Buoy Observations (CRISP-DM Framework)\n"
                          "B.Tech Computer Science Engineering — Data Mining Academic Research Paper | October 2026")
    r_sub.font.name = 'Times New Roman'
    r_sub.font.size = Pt(10)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(80, 80, 80)

    # Callout Banner
    add_callout(doc,
                "1. GEOGRAPHIC PROVENANCE: All observational data originates exclusively from United States territorial waters (NOAA National Data Buoy Center) in the Northwest Atlantic Ocean and Gulf of Mexico. This study contains zero observations from Indian territorial waters.\n"
                "2. ACADEMIC INTEGRITY GUARANTEE: Every quantitative score, table value, rule split, and chart was computed by executing reproducible Python and Orange Data Mining workflows on the raw NOAA telemetry. Zero numbers or experimental outcomes are simulated or fabricated.\n"
                "3. DERIVED RESEARCH LABELS: Cluster groupings and wind condition terciles represent sample-specific statistical percentiles, NOT official maritime safety categories or statutory navigation advisories.\n"
                "4. PROJECT SCOPE BOUNDARY: Inspired by Smart India Hackathon (SIH26176) concepts. Chatbots, autonomous agents, emergency SMS alerts, and satellite Potential Fishing Zone (PFZ) predictions are formally cataloged under Future Scope.",
                title="MANDATORY RESEARCH AND ETHICAL INTEGRITY DISCLOSURE", border_color="C53030", bg_color="FFF8F8")

    # -------------------------------------------------------------
    # ACKNOWLEDGEMENTS
    # -------------------------------------------------------------
    add_header_styled(doc, "Acknowledgements", level=1)
    add_body_p(doc,
               "I would like to express my sincere gratitude to Dr. Abhilasha Deshwar, my teacher and project supervisor, for her invaluable guidance, continuous encouragement, and constructive support throughout the completion of this research project. Her insightful suggestions and academic mentorship have significantly enriched my understanding of data mining methodologies, preprocessing workflows, and their empirical application to marine environmental data analysis. I am deeply thankful for the opportunity to undertake this research under her supervision as part of my undergraduate academic learning. I also extend my sincere appreciation to my department and institution for providing the academic environment, resources, and opportunity to explore this subject.")

    # -------------------------------------------------------------
    # ABSTRACT & KEYWORDS
    # -------------------------------------------------------------
    add_header_styled(doc, "Abstract", level=1)
    add_body_p(doc,
               "Autonomous maritime situational awareness requires resilient, data-driven pipelines capable of extracting actionable intelligence from continuous environmental telemetry. This research investigates whether standard data mining techniques—specifically k-Means unsupervised clustering, Decision Trees (CART), Random Forests, and Gaussian Naive Bayes—can identify physical meteorological patterns and classify observed conditions from in-situ buoy telemetry. Utilizing 3-hourly standard meteorological records from NOAA National Data Buoy Center (NDBC) ERDDAP dataset cwwcNDBCMet covering January to June 2025 across two United States marine stations, this paper resolves real-world sensor non-reporting challenges, audits preprocessing thresholds, and evaluates predictive generalization. Forensic auditing reveals that a 34.01% missingness rate in Orange Data Mining stems from completely unrecorded wave accelerometer payloads (100% missing significant wave height) and localized thermistor absence (73.67% missing sea surface temperature). Eliminating features with over 50% missingness preserves a multi-station core of 1,963 clean records across barometric pressure, wind speed, wind gust, and air temperature. In unsupervised modeling, silhouette optimization confirms an optimal cluster partition at k = 2 (silhouette coefficient = 0.3537), identifying a tranquil warm regime (67.09% of records) and an energetic cool regime (32.91%). Evaluating cluster independence against buoy station identity yields an Adjusted Rand Index (ARI) of -0.0243, proving mathematically that clusters represent shared physical atmospheric states rather than geographic station coordinates. In supervised classification of balanced marine condition terciles, Decision Tree (49.37% CV accuracy) and Random Forest (49.16% CV accuracy) models outperform the 33.47% majority baseline using only non-leaking barometric pressure and air temperature predictors. Crucially, forward chronological evaluation (January–April training vs. May–June testing) shows an accuracy drop to 41.10% and 37.42%, empirically exposing how temporal autocorrelation in consecutive 3-hourly telemetry inflates randomized cross-validation. Controlled experiments further prove that imputing null sensors produces a negligible 0.15% variance delta, while including concurrent wind gusts artificially inflates accuracy to 92.87% through target leakage. These findings establish the necessity of rigorous feature quarantine and chronological validation in operational marine data mining.")

    add_body_p(doc,
               "Data mining, marine meteorology, NOAA NDBC buoy data, Orange Data Mining, k-Means clustering, decision trees, random forests, temporal autocorrelation, feature quarantine, CRISP-DM.",
               bold_prefix="Keywords— ")

    # -------------------------------------------------------------
    # SECTION I: INTRODUCTION
    # -------------------------------------------------------------
    add_header_styled(doc, "I. Introduction", level=1)
    add_body_p(doc,
               "Marine environmental telemetry provides the vital observational foundation for maritime safety, coastal engineering, weather forecasting, and resource management [1], [2]. While spaceborne satellite remote sensing offers synoptic spatial coverage across oceanic basins, in-situ moored buoys and coastal marine platforms maintained by agencies such as the National Oceanic and Atmospheric Administration (NOAA) National Data Buoy Center (NDBC) provide high-precision, continuous temporal ground truth [3]. Moored buoys measure surface wind dynamics, atmospheric barometric pressure, air temperature, and sea surface temperature under extreme oceanic conditions [2], [3].")

    add_body_p(doc,
               "However, real-world oceanographic telemetry presents formidable analytical challenges. Autonomous sensors exposed to corrosive marine environments suffer from biofouling, battery depletion, transmission latency, intermittent dropouts, and mechanical failure [3]. Consequently, operational datasets rarely match theoretical expectations, frequently containing high rates of missing values, truncated observational records, and strong temporal autocorrelation. Extracting actionable intelligence from noisy marine data requires systematic, evidence-based data mining workflows rather than superficial black-box modeling [1], [6].")

    add_body_p(doc,
               "This academic research paper presents a complete, rigorous data mining exploration of in-situ NOAA NDBC buoy telemetry utilizing the Cross-Industry Standard Process for Data Mining (CRISP-DM) framework within Orange Data Mining [6] and Python. Conducted as an undergraduate B.Tech Computer Science engineering research project, this study deliberately prioritizes methodological honesty, mathematical transparency, and reproducibility over inflated operational claims. It investigates the complete data mining lifecycle: forensic data auditing, missing-value thresholding, exploratory physical coupling, unsupervised regime discovery via k-Means clustering, and supervised classification of marine condition terciles.")

    # -------------------------------------------------------------
    # SECTION II: PROBLEM STATEMENT AND RESEARCH OBJECTIVES
    # -------------------------------------------------------------
    add_header_styled(doc, "II. Problem Statement and Research Objectives", level=1)
    add_body_p(doc,
               "The core problem addressed in this study is the reliable extraction of marine meteorological patterns and the classification of observed conditions from noisy in-situ telemetry without falling victim to location shortcuts, temporal data leakage, or unverified data synthesis. In academic machine learning, researchers frequently apply cross-validation algorithms blindly to time-series datasets, generating overly optimistic accuracy scores that fail in operational deployments. Furthermore, sensor outages are often swept aside through blind imputation, introducing bias and misrepresenting underlying physical phenomena.")

    add_body_p(doc,
               "To resolve these challenges, this study addresses the following four research questions (RQs):",
               bold_prefix="Research Formulation— ")
    add_body_p(doc,
               "• RQ1 (Main Question): Can data mining techniques discover meaningful physical patterns in in-situ marine meteorological observations and accurately classify observed condition regimes using surface atmospheric predictors without location shortcuts or data leakage?\n"
               "• RQ2 (Unsupervised Regime Discovery): Does k-Means clustering identify distinct, meteorologically coherent marine weather regimes across multi-station buoy observations, and do these clusters represent shared physical states rather than geographic station coordinates?\n"
               "• RQ3 (Supervised Predictive Capacity): To what extent can independent surface barometric pressure and air temperature measurements classify discretized marine condition terciles above the random majority baseline?\n"
               "• RQ4 (Temporal Generalization vs. CV Optimism): What is the quantitative impact of temporal autocorrelation on model evaluation when comparing standard randomized 10-fold cross-validation against a forward chronological seasonal split?")

    # -------------------------------------------------------------
    # SECTION III: RELATED WORK / LITERATURE REVIEW
    # -------------------------------------------------------------
    add_header_styled(doc, "III. Related Work and Literature Review", level=1)
    add_body_p(doc,
               "Data mining and machine learning in marine meteorology have expanded rapidly alongside modern buoy networks and automated data servers. Meindl and Hamilton [3] established the historical and operational framework of the NOAA NDBC moored buoy and Coastal-Marine Automated Network (C-MAN) stations, highlighting their essential role in numerical weather prediction and satellite validation. Simons [4] detailed the architecture of the Environmental Research Division's Data Access Program (ERDDAP), which revolutionized oceanographic data interoperability by providing RESTful endpoints, standardized ISO 8601 timestamps, and automated format translation for heterogeneous marine datasets.")

    add_body_p(doc,
               "In physical oceanography, the relationship between atmospheric wind forcing and sea-state wave growth represents a foundational principle. In their seminal work, Pierson and Moskowitz [5] introduced the universal wave spectrum for fully developed wind seas, proving that wave energy distribution and significant wave height scale directly and monotonically with sustained wind speed (Hm0 ∝ U10^2). This physical oceanographic derivation confirms that surface wind velocity is the primary energetic driver of sea state, providing a rigorous theoretical foundation for analyzing wind condition terciles as proxies for marine kinetic energy.")

    add_body_p(doc,
               "Unsupervised clustering has been widely investigated for categorizing oceanographic regimes. MacQueen [7] introduced the k-Means partitioning algorithm, which minimizes within-cluster sum of squared Euclidean distances. In environmental applications, feature standardization is universally recognized as mandatory to prevent high-magnitude variables (such as barometric pressure ~1018 hPa) from dominating lower-magnitude variables (such as wind speed ~6 m/s). Rousseeuw [8] established the silhouette coefficient, balancing intra-cluster cohesion against inter-cluster separation to mathematically determine optimal cluster counts without subjective bias. Hubert and Arabie [9] formulated the Adjusted Rand Index (ARI), which provides a chance-corrected mathematical metric to evaluate partition overlap against independent groupings, such as geographic station metadata.")

    add_body_p(doc,
               "In supervised classification, Breiman et al. [10] developed Classification and Regression Trees (CART), offering transparent, rule-based binary recursive splitting based on Gini impurity. Breiman [11] extended this to Random Forests, demonstrating that aggregating 100 de-correlated bootstrap decision trees mitigates variance on noisy environmental observations. Hand and Yu [12] demonstrated that Gaussian Naive Bayes remains a competitive baseline despite its strict independence assumptions. However, recent environmental literature warns against blind cross-validation on continuous sensor streams, noting that temporal autocorrelation between adjacent time steps leads to optimistic validation scores [1], [6].")

    # -------------------------------------------------------------
    # SECTION IV: RESEARCH GAP AND SCOPE DEFINITION
    # -------------------------------------------------------------
    add_header_styled(doc, "IV. Research Gap and Scope Definition", level=1)
    add_body_p(doc,
               "While extensive literature addresses complex deep learning architectures for marine forecasting, a significant gap exists in empirical studies documenting the forensic preprocessing reality of real-world buoy data at the undergraduate engineering level. Many published tutorials gloss over sensor non-reporting, fail to explain missingness diagnostics in visual tools like Orange, or commit subtle data leakage by including concurrent gust measurements or spatial shortcuts.")

    add_body_p(doc,
               "Scope Boundaries (SIH26176 Alignment): This research was inspired by concepts in the Smart India Hackathon problem statement SIH26176 (Agentic-AI Marine Intelligence Platform). However, to maintain academic rigor and feasibility within a B.Tech Data Mining curriculum, the project deliberately restricts its scope to the data mining core (CRISP-DM). Complex multi-agent LLM reasoning, autonomous emergency alert routing, automated vessel navigation, and satellite Potential Fishing Zone (PFZ) advisory generation—which requires fusing multi-spectral satellite chlorophyll-a and sea surface temperature imagery as practiced by INCOIS [13]—are formally and properly demarcated as Future Scope.")

    # -------------------------------------------------------------
    # SECTION V: DATASET DESCRIPTION AND FORENSIC AUDITING
    # -------------------------------------------------------------
    add_header_styled(doc, "V. Dataset Description and Forensic Auditing", level=1)
    add_body_p(doc,
               "The observational data analyzed in this study was retrieved from the NOAA National Data Buoy Center Standard Meteorological Buoy Data archive via the NOAA CoastWatch ERDDAP server (Dataset ID: cwwcNDBCMet) [1]. The data represents 3-hourly nominal surface observations spanning the 181-day period from January 1, 2025 (00:00:00Z) to June 30, 2025 (23:50:00Z). The raw downloaded CSV contains 1,967 rows across 12 attributes formatted in standard NOAA NDBC units [1], [2].")

    add_header_styled(doc, "A. Forensic Resolution of the 1,967 vs. ~4,300 Row Gap", level=2)
    add_body_p(doc,
               "An initial design expectation anticipated approximately ~4,300 rows based on 3 buoy stations over 181 calendar days with 8 observations per day (181 × 8 = 1,448 nominal slots per buoy; 1,448 × 3 = 4,344 records). Forensic auditing of the raw CSV identified two distinct physical causes for the observed 1,967 rows:\n"
               "1. Omission of 3rd Intended Station: The returned ERDDAP payload contained only two stations (Station 42040 and Station 41002); a planned third station was absent (-1,448 records).\n"
               "2. Station 41002 Delayed Deployment: While Station 42040 (Luke Offshore Test Platform in the Mississippi Canyon, Gulf of Mexico, 29.212° N, -88.207° E) operated continuously across all 181 days (1,449 rows, matching nominal expectations), Station 41002 (South Hatteras, Northwest Atlantic Ocean, 31.887° N, -74.921° E) only began reporting on April 27, 2025 at 09:00:00Z. Over 116 days of winter and early spring observations were unrecorded, resulting in an empirical deficit of ~930 records (518 observed rows vs. 1,448 expected).")

    add_header_styled(doc, "B. Mathematical Reconciliation of Orange's '34% Missing Values' Diagnostic", level=2)
    add_body_p(doc,
               "When raw.csv is loaded into Orange Data Mining [6], the feature statistics window reports an overall missingness rate of '34% missing values'. This diagnostic was audited and reconciled. Orange treats the 11 numeric attributes as the feature domain X (treating 'time (UTC)' as meta), resulting in 1,967 × 11 = 21,637 total feature cells. The actual missing cells across X are:\n"
               "• WVHT (m), DPD (s), APD (s): 1,967 missing each (100.0% unrecorded; wave accelerometer payloads were uninstalled or offline on both platforms).\n"
               "• WTMP (degree_C): 1,449 missing (73.67% overall; Station 42040 is a fixed platform lacking a hull-mounted water thermistor).\n"
               "• WSPD, GST, BAR, ATMP: 2 missing cells each (0.10%, occurring across 4 distinct records at Station 42040).\n"
               "Summing these missing cells yields exactly 7,358 missing cells out of 21,637 feature cells: (7,358 / 21,637) × 100 = 34.0066% (34.01%), providing an exact mathematical reconciliation of Orange's diagnostic.")

    # -------------------------------------------------------------
    # SECTION VI: MATERIALS AND METHODS
    # -------------------------------------------------------------
    add_header_styled(doc, "VI. Materials and Methods", level=1)
    add_body_p(doc,
               "The data mining methodology utilizes a hybrid analytical pipeline implemented in Orange Data Mining (v3.40.0) [6] and Python (scikit-learn, pandas, numpy). The pipeline consists of four primary analytical components:")

    add_body_p(doc,
               "1) Feature Standardization: Features for distance-based clustering were normalized using z-score standardization:\n"
               "   z = (x - μ) / σ\n"
               "This ensures that barometric pressure (mean ~1018.7 hPa) and wind speed (mean ~5.9 m/s) contribute proportionally to Euclidean distance calculations.\n\n"
               "2) k-Means Partitioning & Silhouette Optimization: k-Means iteratively minimizes within-cluster inertia across k = 2 to 6. Cluster quality was evaluated using Rousseeuw's silhouette coefficient [8]:\n"
               "   s(i) = (b(i) - a(i)) / max(a(i), b(i))\n"
               "where a(i) is the mean intra-cluster distance and b(i) is the mean nearest-cluster distance.\n\n"
               "3) Adjusted Rand Index (ARI): To test whether clustering merely learned geographic station identities, the Adjusted Rand Index [9] was computed between cluster assignments and buoy station labels:\n"
               "   ARI = (Index - Expected Index) / (Max Index - Expected Index)\n"
               "An ARI near 0 indicates partition independence from station geography.\n\n"
               "4) Supervised Classifiers: Three algorithms were implemented:\n"
               "   • Decision Tree (CART) [10]: Constrained to max_depth = 5 and min_samples_leaf = 20 to prevent leaf overfitting.\n"
               "   • Random Forest [11]: Ensemble of 100 de-correlated trees trained via bootstrap aggregating.\n"
               "   • Gaussian Naive Bayes [12]: Class-conditional normal probability density estimation.")

    # -------------------------------------------------------------
    # SECTION VII: DATA PREPROCESSING AND CLEANING
    # -------------------------------------------------------------
    add_header_styled(doc, "VII. Data Preprocessing and Cleaning", level=1)
    add_body_p(doc,
               "Data preprocessing decisions were guided by empirical evidence documented in DECISIONS.md:\n"
               "1. Missingness Thresholding (>50% Rule): Attributes with missingness exceeding 50% were eliminated. WVHT, DPD, and APD (100% missing) were purged entirely.\n"
               "2. Geographic Preservation vs. WTMP: Requiring complete cases on WTMP forces listwise deletion of all 1,449 rows of Station 42040 (100% row loss), collapsing the dataset into an isolated single-buoy Atlantic sample. To preserve spatial validity, the primary Core Pipeline retains WSPD, GST, BAR, and ATMP across both stations, while WTMP is evaluated in an isolated Atlantic subset (N=518).\n"
               "3. Plausibility Screening: Heuristic screening confirmed zero violations across active features: WSPD [0, 50] m/s, GST [0, 70] m/s, BAR [900, 1100] hPa, ATMP [-40, 50] °C, WTMP [-2, 40] °C.\n"
               "4. Outage Filtering: Filtering 4 records with sensor dropouts at Station 42040 yielded 1,963 clean records (99.80% retention).")

    # Table 1: Cleaning Accounting
    tbl1 = doc.add_table(rows=5, cols=6)
    t1_headers = ["Pipeline", "Station Scope", "Raw Rows", "Retained Rows", "Dropped Rows", "Retention Rate"]
    t1_rows = [
        t1_headers,
        ["Core Pipeline", "All Stations (Multi-Buoy)", "1,967", "1,963", "4", "99.80%"],
        ["Core Pipeline", "Station 42040 (Gulf of Mexico)", "1,449", "1,445", "4", "99.72%"],
        ["Core Pipeline", "Station 41002 (Atlantic Ocean)", "518", "518", "0", "100.00%"],
        ["WTMP Pipeline", "All Stations", "1,967", "518", "1,449", "26.33%"]
    ]
    for r_idx, row in enumerate(t1_rows):
        for c_idx, val in enumerate(row):
            tbl1.cell(r_idx, c_idx).text = val
    format_table(tbl1)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    p_t1_cap = doc.add_paragraph("Table I: Observational Row Accounting Across Preprocessing Pipelines.")
    p_t1_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t1_cap.runs[0].font.size = Pt(8.5); p_t1_cap.runs[0].font.italic = True

    # -------------------------------------------------------------
    # SECTION VIII: EXPERIMENTAL SETUP AND ORANGE WORKFLOW
    # -------------------------------------------------------------
    add_header_styled(doc, "VIII. Experimental Setup and Orange Workflow", level=1)
    add_body_p(doc,
               "The complete experimental workflow was modeled visually in Orange Data Mining [6] and saved as a native workflow schema (marine_project.ows). The schema contains 11 nodes linked across 10 functional signal channels:\n"
               "• Data Ingest & Audit: A File widget ingests cleaned_core.csv, feeding a Data Info widget to verify zero missingness across 1,963 rows.\n"
               "• Feature Selection: A Select Columns widget routes BAR and ATMP to Features, target terciles to Target, and quarantines WSPD, GST, and station identifiers to Metas.\n"
               "• Normalization: A Preprocess widget applies standardization (mean=0, std=1).\n"
               "• Unsupervised Branch: Standardized features route to a k-Means widget (k=2..6, random_state=42) and a Scatter Plot widget.\n"
               "• Supervised Branch: Features feed Tree, Random Forest, and Naive Bayes learners into a Test and Score evaluation widget connected to a Confusion Matrix widget.")

    # -------------------------------------------------------------
    # SECTION IX: RESULTS AND EMPIRICAL FINDINGS
    # -------------------------------------------------------------
    add_header_styled(doc, "IX. Results and Empirical Findings", level=1)

    add_header_styled(doc, "A. Exploratory Distributions and Physical Coupling", level=2)
    add_body_p(doc,
               "Table II reports the descriptive statistics for the core observational parameters. Surface wind speed exhibits moderate right-skewness (+0.463) with a sample mean of 5.92 m/s and a maximum of 15.30 m/s. Barometric pressure follows a Gaussian-like distribution centered at 1018.73 hPa (std = 4.59 hPa). Figure 1 illustrates the histograms and kernel density estimates.")

    # Table 2: Descriptive Stats
    tbl2 = doc.add_table(rows=6, cols=9)
    t2_headers = ["Attribute", "Scope", "N", "Mean", "Std Dev", "Median", "IQR", "Min", "Max"]
    t2_rows = [
        t2_headers,
        ["WSPD (m/s)", "All Stations", "1,963", "5.921", "2.755", "5.700", "3.700", "0.100", "15.300"],
        ["GST (m/s)", "All Stations", "1,963", "7.561", "3.396", "7.200", "4.300", "0.700", "19.800"],
        ["BAR (hPa)", "All Stations", "1,963", "1018.725", "4.588", "1018.800", "5.900", "1000.700", "1033.200"],
        ["ATMP (°C)", "All Stations", "1,963", "22.731", "5.095", "23.600", "6.500", "3.200", "30.900"],
        ["WTMP (°C)", "Station 41002", "518", "25.730", "2.228", "25.800", "4.300", "21.700", "29.700"]
    ]
    for r_idx, row in enumerate(t2_rows):
        for c_idx, val in enumerate(row):
            tbl2.cell(r_idx, c_idx).text = val
    format_table(tbl2)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    p_t2_cap = doc.add_paragraph("Table II: Summary Statistics of Observed Marine Meteorological Variables.")
    p_t2_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t2_cap.runs[0].font.size = Pt(8.5); p_t2_cap.runs[0].font.italic = True

    # Embed Figure 1
    add_figure_with_caption(doc,
                            os.path.join("ResearchPaper", "figures", "fig01_histograms_core_features.png"),
                            "Figure 1: Histograms and kernel density distributions of core buoy features (N=1,963).")

    add_body_p(doc,
               "Figure 2 illustrates cross-station comparative box plots, displaying the broad seasonal air temperature range of Station 42040 in the Gulf of Mexico compared to the late-spring maritime warmth of Station 41002 in the Atlantic. Figure 3 presents the bivariate relationships: the left panel visually confirms that WVHT contains zero observations, while the right panel displays near-perfect linear proportionality between wind speed and wind gust (r = +0.957; GST = 1.18 × WSPD + 0.58). Figure 4 and Figure 5 show the multi-variable correlation heatmaps and continuous 6-month time series.")

    # Embed Figures 2, 3, 4, 5
    add_figure_with_caption(doc,
                            os.path.join("ResearchPaper", "figures", "fig02_boxplots_by_station.png"),
                            "Figure 2: Distributional comparison of core meteorological features across buoy stations.")

    add_figure_with_caption(doc,
                            os.path.join("ResearchPaper", "figures", "fig03_scatter_wspd_wvht_gst.png"),
                            "Figure 3: Scatter plot of WSPD vs. missing WVHT (left) and WSPD vs. GST with regression fit (right).")

    add_figure_with_caption(doc,
                            os.path.join("ResearchPaper", "figures", "fig04_correlation_matrix.png"),
                            "Figure 4: Pearson correlation matrices for core features (left) and Atlantic SST subset (right).")

    add_figure_with_caption(doc,
                            os.path.join("ResearchPaper", "figures", "fig05_timeseries_per_station.png"),
                            "Figure 5: Six-month continuous temporal profiles of WSPD, BAR, and ATMP across both buoys.")

    add_header_styled(doc, "B. Unsupervised k-Means Clustering and Regime Discovery", level=2)
    add_body_p(doc,
               "Silhouette optimization across k = 2 to 6 identified k = 2 as the global mathematical optimum (silhouette = 0.3537, inertia = 5,095.42), as presented in Table III and Figure 6. Cluster profiles in physical units are detailed in Table IV and visualized in Figure 7.")

    # Table 3: Silhouette
    tbl3 = doc.add_table(rows=6, cols=4)
    t3_headers = ["Cluster Count (k)", "Silhouette Score", "Within-Cluster Inertia", "Optimization Status"]
    t3_rows = [
        t3_headers,
        ["k = 2", "0.3537", "5,095.42", "Global Mathematical Optimum"],
        ["k = 3", "0.3338", "3,716.41", "Secondary High Silhouette"],
        ["k = 4", "0.2819", "2,995.17", "Sub-optimal Partition"],
        ["k = 5", "0.2813", "2,540.74", "Fragmented Regimes"],
        ["k = 6", "0.2869", "2,209.61", "Over-partitioned Clusters"]
    ]
    for r_idx, row in enumerate(t3_rows):
        for c_idx, val in enumerate(row):
            tbl3.cell(r_idx, c_idx).text = val
    format_table(tbl3)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    p_t3_cap = doc.add_paragraph("Table III: Cluster Evaluation Metrics Across k = 2 to 6 (random_state=42).")
    p_t3_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t3_cap.runs[0].font.size = Pt(8.5); p_t3_cap.runs[0].font.italic = True

    # Embed Figure 6 & 7
    add_figure_with_caption(doc,
                            os.path.join("ResearchPaper", "figures", "fig06_k_selection_silhouette_elbow.png"),
                            "Figure 6: Silhouette coefficients and within-cluster inertia across k = 2 to 6.")

    # Table 4: Cluster Profiles
    tbl4 = doc.add_table(rows=3, cols=7)
    t4_headers = ["Cluster Label", "Record Count", "Proportion", "Mean WSPD (m/s)", "Mean GST (m/s)", "Mean BAR (hPa)", "Mean ATMP (°C)"]
    t4_rows = [
        t4_headers,
        ["Cluster 1 (Tranquil)", "1,317", "67.09%", "4.455 ± 1.715", "5.698 ± 1.922", "1018.586 ± 3.510", "24.366 ± 3.821"],
        ["Cluster 2 (Energetic)", "646", "32.91%", "8.911 ± 1.933", "11.359 ± 2.449", "1019.010 ± 6.228", "19.397 ± 5.708"]
    ]
    for r_idx, row in enumerate(t4_rows):
        for c_idx, val in enumerate(row):
            tbl4.cell(r_idx, c_idx).text = val
    format_table(tbl4)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    p_t4_cap = doc.add_paragraph("Table IV: Quantitative Meteorological Profiles of Discovered k = 2 Regimes.")
    p_t4_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t4_cap.runs[0].font.size = Pt(8.5); p_t4_cap.runs[0].font.italic = True

    add_figure_with_caption(doc,
                            os.path.join("ResearchPaper", "figures", "fig07_cluster_scatter_k2.png"),
                            "Figure 7: Bivariate feature distributions of discovered k = 2 clusters with marked centroids (X).")

    add_body_p(doc,
               "Cross-Tabulation & Geographic Independence: Cross-tabulating Cluster 1 (401 at Station 41002, 916 at Station 42040) and Cluster 2 (117 at Station 41002, 529 at Station 42040) yielded an Adjusted Rand Index of ARI = -0.0243. Because ARI is near zero, this mathematically demonstrates that the unsupervised clusters do not recreate station geography. Both buoys experience both weather regimes.")

    add_header_styled(doc, "C. Supervised Classification Benchmark", level=2)
    add_body_p(doc,
               "Discretizing wind speed established three equal-frequency terciles: Low (≤ 4.60 m/s, N=654, 33.32%), Mid (4.60–6.90 m/s, N=657, 33.47%), and High (> 6.90 m/s, N=652, 33.21%). Table V presents comparative model performance across stratified 10-fold cross-validation and chronological splitting. Figure 8 depicts the corresponding confusion matrices.")

    # Table 5: Classification Metrics
    tbl5 = doc.add_table(rows=9, cols=7)
    t5_headers = ["Algorithm", "Evaluation Protocol", "Accuracy", "Macro Precision", "Macro Recall", "Macro F1", "Per-Class F1 (Low/Mid/High)"]
    t5_rows = [
        t5_headers,
        ["Majority Baseline", "Stratified 10-Fold CV", "33.47%", "0.1116", "0.3333", "0.1672", "0.000 / 0.502 / 0.000"],
        ["Decision Tree (CART)", "Stratified 10-Fold CV", "49.37%", "0.5195", "0.4940", "0.4885", "0.471 / 0.469 / 0.526"],
        ["Random Forest (100)", "Stratified 10-Fold CV", "49.16%", "0.4922", "0.4920", "0.4898", "0.504 / 0.423 / 0.542"],
        ["Gaussian Naive Bayes", "Stratified 10-Fold CV", "44.52%", "0.4553", "0.4457", "0.4336", "0.507 / 0.294 / 0.501"],
        ["Majority Baseline", "Chronological Split", "24.03%", "0.0801", "0.3333", "0.1292", "0.000 / 0.000 / 0.388"],
        ["Decision Tree (CART)", "Chronological Split", "41.10%", "0.3861", "0.4325", "0.3668", "0.555 / 0.120 / 0.426"],
        ["Random Forest (100)", "Chronological Split", "37.42%", "0.3707", "0.4061", "0.3581", "0.460 / 0.189 / 0.425"],
        ["Gaussian Naive Bayes", "Chronological Split", "30.27%", "0.3361", "0.3372", "0.2871", "0.154 / 0.376 / 0.332"]
    ]
    for r_idx, row in enumerate(t5_rows):
        for c_idx, val in enumerate(row):
            tbl5.cell(r_idx, c_idx).text = val
    format_table(tbl5)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    p_t5_cap = doc.add_paragraph("Table V: Supervised Classification Performance Benchmarks on Marine Condition Terciles.")
    p_t5_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t5_cap.runs[0].font.size = Pt(8.5); p_t5_cap.runs[0].font.italic = True

    add_figure_with_caption(doc,
                            os.path.join("ResearchPaper", "figures", "fig08_confusion_matrices.png"),
                            "Figure 8: Confusion matrices for Stratified 10-Fold CV (top) and Chronological Split (bottom).")

    add_header_styled(doc, "D. Controlled Extra Experiments: Leakage and Null Features", level=2)
    add_body_p(doc,
               "Table VI reports the results of three controlled experiments evaluating zero-variance feature imputation, spatial shortcuts, and target leakage.")

    # Table 6: Extra Experiments
    tbl6 = doc.add_table(rows=5, cols=5)
    t6_headers = ["Experiment Suite", "10-Fold CV Acc", "10-Fold F1", "Chrono Split Acc", "Chrono Split F1"]
    t6_rows = [
        t6_headers,
        ["Baseline Predictors (BAR, ATMP)", "49.16%", "0.4898", "37.42%", "0.3581"],
        ["(i) Add DPD + APD (Null Sensors Imputed)", "49.31%", "0.4926", "39.26%", "0.3710"],
        ["(ii) Add Station (Location Shortcut)", "51.20%", "0.5113", "44.38%", "0.4400"],
        ["(iii) Add GST (Near-Leakage Feature)", "92.87%", "0.9287", "92.84%", "0.9284"]
    ]
    for r_idx, row in enumerate(t6_rows):
        for c_idx, val in enumerate(row):
            tbl6.cell(r_idx, c_idx).text = val
    format_table(tbl6)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    p_t6_cap = doc.add_paragraph("Table VI: Controlled Extra Experiments Evaluating Feature Leakage and Spatial Shortcuts.")
    p_t6_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t6_cap.runs[0].font.size = Pt(8.5); p_t6_cap.runs[0].font.italic = True

    # -------------------------------------------------------------
    # SECTION X: DISCUSSION
    # -------------------------------------------------------------
    add_header_styled(doc, "X. Discussion", level=1)
    add_body_p(doc,
               "The empirical findings provide clear answers to the research questions while highlighting vital methodological principles for environmental data mining.")

    add_header_styled(doc, "A. Physical Meteorology of Extracted Tree Rules", level=2)
    add_body_p(doc,
               "The Decision Tree fitted on the historical baseline extracted three primary physical decision paths:\n"
               "• Cyclonic Low-Pressure Path: When BAR ≤ 1016.75 hPa, the model consistently assigns class 'High' (turbulent marine conditions). This mirrors atmospheric physics: dynamic low-pressure troughs drive steep pressure gradients and energetic wind fields.\n"
               "• Anticyclonic Summer Ridge Path: When BAR > 1016.75 hPa and ATMP > 24.25 °C, the model assigns class 'Low' (calm conditions). This reflects stable subtropical high-pressure ridges characterized by subsidence and light surface winds.\n"
               "• Transitional Gradient Path: Moderate pressure (1016.75 < BAR ≤ 1025.95 hPa) coupled with moderate temperature (21.75 < ATMP ≤ 24.25 °C) maps to class 'Mid'.")

    add_header_styled(doc, "B. The Deceptive Optimism of Randomized Cross-Validation", level=2)
    add_body_p(doc,
               "The stark performance drop between Stratified 10-Fold CV (49.37% Decision Tree, 49.16% Random Forest) and forward Chronological Splitting (41.10% Decision Tree, 37.42% Random Forest) exposes the profound impact of temporal autocorrelation. Marine atmospheric fronts persist over synoptic time horizons of 24 to 72 hours. In randomized k-fold partitioning, consecutive 3-hourly measurements from the exact same weather system are scattered into both training and validation folds. The model effectively interpolates between adjacent hours, artificially inflating validation accuracy. When evaluated chronologically (training on Jan–Apr, testing on May–Jun), the model faces real forward seasonal distribution shift (winter storms transitioning to summer ridges), revealing true operational generalization capacity.")

    add_header_styled(doc, "C. What the Results Establish vs. What They Do NOT Establish", level=2)
    add_body_p(doc,
               "What is Established: (1) Surface atmospheric variables (pressure and temperature) contain genuine, statistically significant predictive signals for sea-state kinetic energy regimes, achieving ~49% accuracy against a 33.5% random baseline without spatial coordinates. (2) k-Means clustering uncovers coherent multi-station meteorological regimes independent of station geography (ARI = -0.0243).\n"
               "What is NOT Established: (1) These models do NOT establish an operational wave forecasting system. Wave height was unrecorded, and wind terciles are not statutory maritime safety codes. (2) These results do NOT predict fish abundance or Potential Fishing Zones (PFZs). Marine productivity depends on upwelling, bathymetry, and satellite-measured chlorophyll-a frontogenesis [13], which were outside the scope of this study.")

    # -------------------------------------------------------------
    # SECTION XI: METHODOLOGICAL LIMITATIONS
    # -------------------------------------------------------------
    add_header_styled(doc, "XI. Methodological Limitations and Ethical Safeguards", level=1)
    add_body_p(doc,
               "In compliance with scientific integrity standards, the following limitations are candidly disclosed:\n"
               "1. Geographic Restriction: Data originates exclusively from United States Atlantic and Gulf waters. Findings cannot be generalized to Indian waters, which exhibit distinct monsoon wind reversals.\n"
               "2. Temporal Horizon: The dataset spans only 6 months (January–June 2025), capturing a single winter-to-summer transition rather than multi-year climatological cycles.\n"
               "3. Station Attrition: Only 2 buoys were captured rather than 3, with Station 41002 suffering an extensive 116-day telemetry gap.\n"
               "4. Derived Tercile Target: The classification labels represent statistical percentiles of this sample, NOT certified World Meteorological Organization (WMO) sea-state codes [14].\n"
               "5. Operational Disclaimer: Models must NEVER be deployed for vessel navigation clearance, maritime search-and-rescue, or life-safety alerts.")

    # -------------------------------------------------------------
    # SECTION XII: CONCLUSION AND FUTURE SCOPE
    # -------------------------------------------------------------
    add_header_styled(doc, "XII. Conclusion and Future Scope", level=1)
    add_body_p(doc,
               "Conclusion: This research successfully demonstrates the complete data mining lifecycle applied to in-situ marine meteorological buoy telemetry. Using Orange Data Mining and Python, the study forensicly resolved a 34.01% missingness diagnostic, proved that unsupervised k-Means clustering uncovers cross-station meteorological regimes (ARI = -0.0243), and benchmarked supervised classifiers on marine condition terciles. Furthermore, comparing randomized cross-validation against chronological splitting empirically demonstrated the deceptive optimism caused by temporal autocorrelation.")

    add_body_p(doc,
               "Future Scope (SIH26176 Alignment):\n"
               "1. Task B (Satellite Oceanography): Fusing satellite Sea Surface Temperature (SST) and Chlorophyll-a telemetry to model Potential Fishing Zones (PFZs), integrating INCOIS advisory methods [13].\n"
               "2. High-Frequency Telemetry: Integrating 10-minute continuous buoy streams and evaluating deep recurrent neural networks (LSTM, GRU, Transformers) for sequential forecasting.\n"
               "3. Multi-Agent Systems: Implementing autonomous agentic routing and conversational community alert distribution as envisioned in SIH26176.")

    # -------------------------------------------------------------
    # SECTION XIII: REFERENCES
    # -------------------------------------------------------------
    add_header_styled(doc, "References", level=1)
    refs = [
        "[1] National Oceanic and Atmospheric Administration (NOAA) CoastWatch / Environmental Research Division (ERD), \"NDBC Standard Meteorological Buoy Data (Dataset ID: cwwcNDBCMet),\" NOAA CoastWatch ERDDAP Data Server, 2025. [Online]. Available: https://coastwatch.pfeg.noaa.gov/erddap/tabledap/cwwcNDBCMet.html. Accessed: Oct. 12, 2026.",
        "[2] National Oceanic and Atmospheric Administration (NOAA) National Data Buoy Center (NDBC), \"NDBC Moored Buoy and C-MAN Station Meteorological Data Descriptions and Instrumentation Specifications,\" National Weather Service, Stennis Space Center, MS, Tech. Doc., 2025. [Online]. Available: https://www.ndbc.noaa.gov/measdes.shtml. Accessed: Oct. 12, 2026.",
        "[3] E. A. Meindl and G. D. Hamilton, \"Programs of the National Data Buoy Center,\" Bulletin of the American Meteorological Society, vol. 73, no. 7, pp. 985–993, Jul. 1992. doi: 10.1175/1520-0477(1992)073<0985:POTNDB>2.0.CO;2.",
        "[4] R. Simons, \"ERDDAP: A Broker to Oceanographic and Climate Data,\" in Proc. Ocean Sciences Meeting / NOAA Environmental Software Development, Pacific Grove, CA: NOAA NMFS SWFSC ERD, 2011. [Online]. Available: https://coastwatch.pfeg.noaa.gov/erddap/index.html. Accessed: Oct. 12, 2026.",
        "[5] W. J. Pierson and L. Moskowitz, \"A proposed spectral form for fully developed wind seas based on the similarity theory of S. A. Kitaigorodskii,\" Journal of Geophysical Research, vol. 69, no. 24, pp. 5181–5190, Dec. 1964. doi: 10.1029/JZ069i024p05181.",
        "[6] J. Demšar, T. Curk, A. Erjavec, Č. Gorup, T. Hočevar, M. Milutinovič, M. Možina, M. Polajnar, M. Toplak, A. Starič, M. Štajdohar, L. Umek, L. Žagar, J. Žbontar, M. Žitnik, and B. Zupan, \"Orange: Data Mining Toolbox in Python,\" Journal of Machine Learning Research, vol. 14, no. 1, pp. 2349–2353, Aug. 2013. [Online]. Available: http://jmlr.org/papers/v14/demsar13a.html.",
        "[7] J. MacQueen, \"Some methods for classification and analysis of multivariate observations,\" in Proc. Fifth Berkeley Symp. on Mathematical Statistics and Probability, vol. 1, Berkeley, CA: Univ. of California Press, 1967, pp. 281–297.",
        "[8] P. J. Rousseeuw, \"Silhouettes: A graphical aid to the interpretation and validation of cluster analysis,\" Journal of Computational and Applied Mathematics, vol. 20, pp. 53–65, Nov. 1987. doi: 10.1016/0377-0427(87)90125-7.",
        "[9] L. Hubert and P. Arabie, \"Comparing partitions,\" Journal of Classification, vol. 2, no. 1, pp. 193–218, Dec. 1985. doi: 10.1007/BF01908075.",
        "[10] L. Breiman, J. H. Friedman, R. A. Olshen, and C. J. Stone, Classification and Regression Trees. Belmont, CA: Wadsworth & Brooks/Cole Advanced Books & Software, 1984.",
        "[11] L. Breiman, \"Random Forests,\" Machine Learning, vol. 45, no. 1, pp. 5–32, Oct. 2001. doi: 10.1023/A:1010933404324.",
        "[12] D. J. Hand and K. Yu, \"Idiot's' Bayes—not so stupid after all?,\" International Statistical Review, vol. 69, no. 3, pp. 385–398, Dec. 2001. doi: 10.1111/j.1751-5823.2001.tb00465.x.",
        "[13] Indian National Centre for Ocean Information Services (INCOIS), \"Potential Fishing Zone (PFZ) Advisory Mission & Methodology,\" Ministry of Earth Sciences (MoES), Govt. of India, Hyderabad, Tech. Rep., 2025. [Online]. Available: https://incois.gov.in/MarineFisheries/PfzAdvisory. Accessed: Oct. 12, 2026.",
        "[14] World Meteorological Organization (WMO), Guide to Wave Analysis and Forecasting, 3rd ed., WMO-No. 702. Geneva, Switzerland: Secretariat of the World Meteorological Organization, 2018."
    ]
    for r in refs:
        p_ref = doc.add_paragraph(r)
        p_ref.paragraph_format.left_indent = Inches(0.4)
        p_ref.paragraph_format.first_line_indent = Inches(-0.4)
        p_ref.paragraph_format.space_after = Pt(4)
        p_ref.runs[0].font.name = 'Times New Roman'
        p_ref.runs[0].font.size = Pt(8.5)

    out_docx = os.path.join("ResearchPaper", "Research_Paper.docx")
    doc.save(out_docx)
    print(f"Successfully generated {out_docx}!")

if __name__ == "__main__":
    build_paper()
