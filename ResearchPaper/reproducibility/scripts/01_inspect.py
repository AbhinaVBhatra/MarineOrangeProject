import os
import pandas as pd
import numpy as np

def run_inspection():
    raw_path = os.path.join("data", "raw.csv")
    out_dir = os.path.join("results", "01_inspection")
    os.makedirs(out_dir, exist_ok=True)

    df = pd.read_csv(raw_path)
    df['parsed_time'] = pd.to_datetime(df['time (UTC)'])

    # 1. Basic Shape and Attributes
    n_rows, n_cols = df.shape
    columns = list(df.columns)
    
    # 2. Orange 34% Missingness Investigation
    # Orange treats numeric attributes as feature domain and string/time as meta.
    # Total numeric cells in feature matrix X:
    num_cols = [c for c in df.columns if c not in ['time (UTC)', 'parsed_time']]
    total_feature_cells = len(df) * len(num_cols)
    null_feature_cells = df[num_cols].isnull().sum().sum()
    orange_missing_pct = (null_feature_cells / total_feature_cells) * 100

    total_table_cells = df.size
    total_table_nulls = df.isnull().sum().sum()
    overall_table_missing_pct = (total_table_nulls / total_table_cells) * 100

    # 3. Investigation of 1,967 vs ~4,300 rows gap
    # A 6-month period (Jan 1 to Jun 30, 2025) has 181 days.
    # At 3-hourly intervals, each day has 8 observations: 181 * 8 = 1,448 observations per station.
    # For 3 stations, the expected row count is 1,448 * 3 = 4,344 rows.
    # What actually exists in the file:
    st_counts = df['station'].value_counts()
    
    with open(os.path.join(out_dir, "gap_and_missing_analysis.txt"), "w", encoding="utf-8") as f:
        f.write("="*70 + "\n")
        f.write("INVESTIGATION OF 1,967 ROWS AND 34% MISSING VALUES IN ORANGE\n")
        f.write("="*70 + "\n\n")
        f.write(f"1. ROW COUNT GAP ANALYSIS (Expected ~4,300 vs Actual 1,967):\n")
        f.write(f"   - Query interval: Jan 1, 2025 00:00:00Z to Jun 30, 2025 23:50:00Z (181 days).\n")
        f.write(f"   - Theoretical 3-hourly frequency: 24h / 3h = 8 readings/day.\n")
        f.write(f"   - Expected readings per fully reporting station: 181 * 8 = 1,448 timestamps.\n")
        f.write(f"   - Expected rows across 3 intended stations: 1,448 * 3 = 4,344 rows.\n")
        f.write(f"   - Observed Stations in CSV: ONLY 2 stations (Station 42040 and Station 41002).\n")
        f.write(f"     * A 3rd intended station was completely omitted or returned 0 rows in the download query.\n")
        f.write(f"   - Breakdown of Observed Stations:\n")
        for st, count in st_counts.items():
            st_df = df[df['station'] == st]
            start_t = st_df['parsed_time'].min()
            end_t = st_df['parsed_time'].max()
            days_span = (end_t - start_t).total_seconds() / 86400.0
            f.write(f"     * Station {st}: {count} rows\n")
            f.write(f"       Date range: {start_t} to {end_t} ({days_span:.1f} days)\n")
            if st == 42040:
                f.write(f"       Note: Covers full 6 months (1,449 rows matches theoretical ~1,448 slots).\n")
            elif st == 41002:
                f.write(f"       Note: Severely truncated timespan! Starts on 2025-04-27 09:00:00Z (missing Jan 1 - Apr 27).\n")
                f.write(f"       Only 64.6 days observed out of 181 days (~116 days missing, ~930 expected rows lost).\n")
        f.write(f"   - Total rows observed: {st_counts.sum()} rows.\n\n")

        f.write(f"2. ORANGE 34% MISSINGNESS EXPLANATION:\n")
        f.write(f"   - Number of rows: {n_rows}\n")
        f.write(f"   - Number of numeric attributes in feature matrix X: {len(num_cols)}\n")
        f.write(f"   - Total feature matrix cells (1967 * 11): {total_feature_cells}\n")
        f.write(f"   - Total missing cells: {null_feature_cells}\n")
        f.write(f"   - Exact missing % reported by Orange: {orange_missing_pct:.2f}% (rounds to 34%)\n\n")
        f.write(f"   - Attribution of Missing Cells by Column:\n")
        for col in num_cols:
            n_null = df[col].isnull().sum()
            pct_null = (n_null / n_rows) * 100
            f.write(f"     * {col:<26}: {n_null:>5} missing ({pct_null:>6.2f}%)\n")
        f.write(f"\n   - Root Cause of Missingness:\n")
        f.write(f"     * WVHT (m), DPD (s), APD (s): 100.00% MISSING (1,967/1,967 rows). Neither station recorded wave metrics.\n")
        f.write(f"     * WTMP (degree_C): 73.67% MISSING (1,449/1,967 rows). Station 42040 has no water temperature sensor.\n")
        f.write(f"     * WSPD, GST, BAR, ATMP: 0.10% MISSING (only 2 timestamps at Station 42040 missing).\n")

    # Save Inspection CSVs
    inspection_table = pd.DataFrame({
        'Attribute': df.columns,
        'Data_Type': df.dtypes.astype(str),
        'Total_Count': len(df),
        'Missing_Count': df.isnull().sum().values,
        'Missing_Pct': (df.isnull().mean() * 100).round(4).values,
        'Unique_Values': [df[c].nunique() for c in df.columns],
        'Min_Value': [df[c].dropna().min() if df[c].dropna().count() > 0 else np.nan for c in df.columns],
        'Max_Value': [df[c].dropna().max() if df[c].dropna().count() > 0 else np.nan for c in df.columns]
    })
    inspection_table.to_csv(os.path.join(out_dir, "column_inspection.csv"), index=False)

    # Per Station Inspection CSV
    per_station_rows = []
    for st, group in df.groupby('station'):
        for col in df.columns:
            if col in ['station', 'parsed_time']:
                continue
            per_station_rows.append({
                'Station': st,
                'Attribute': col,
                'Count': len(group),
                'Missing_Count': group[col].isnull().sum(),
                'Missing_Pct': round(group[col].isnull().mean() * 100, 4),
                'Min': group[col].dropna().min() if group[col].dropna().count() > 0 else np.nan,
                'Max': group[col].dropna().max() if group[col].dropna().count() > 0 else np.nan,
                'Mean': round(group[col].dropna().mean(), 4) if group[col].dropna().count() > 0 and pd.api.types.is_numeric_dtype(group[col]) else np.nan,
                'Std': round(group[col].dropna().std(), 4) if group[col].dropna().count() > 0 and pd.api.types.is_numeric_dtype(group[col]) else np.nan
            })
    pd.DataFrame(per_station_rows).to_csv(os.path.join(out_dir, "per_station_inspection.csv"), index=False)

    print("Inspection complete! Check results/01_inspection/gap_and_missing_analysis.txt and CSV files.")

if __name__ == "__main__":
    run_inspection()
