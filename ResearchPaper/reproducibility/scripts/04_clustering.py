import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples, adjusted_rand_score

# Styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'

def run_clustering():
    data_path = os.path.join("data", "cleaned_core.csv")
    out_dir = os.path.join("results", "04_clustering")
    os.makedirs(out_dir, exist_ok=True)

    df = pd.read_csv(data_path)
    feature_cols = ['WSPD (m s-1)', 'GST (m s-1)', 'BAR (hPa)', 'ATMP (degree_C)']
    X_raw = df[feature_cols].values

    # Step 1: Standardise (Mean = 0, Std = 1)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_raw)

    # Step 2: k-Means for k = 2..6 (random_state=42)
    k_range = range(2, 7)
    silhouette_scores = {}
    inertias = {}
    models = {}

    for k in k_range:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = km.fit_predict(X_scaled)
        sil = silhouette_score(X_scaled, labels)
        silhouette_scores[k] = sil
        inertias[k] = km.inertia_
        models[k] = (km, labels)

    # Save Silhouette table
    sil_df = pd.DataFrame({
        'k': list(k_range),
        'Silhouette_Score': [round(silhouette_scores[k], 4) for k in k_range],
        'Inertia': [round(inertias[k], 2) for k in k_range]
    })
    sil_df.to_csv(os.path.join(out_dir, "silhouette_scores.csv"), index=False)

    # Plot Silhouette Scores & Elbow Curve
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    ax1.plot(list(k_range), [silhouette_scores[k] for k in k_range], 'o-', color='#1f77b4', linewidth=2, markersize=8)
    best_k_sil = max(silhouette_scores, key=silhouette_scores.get)
    ax1.axvline(best_k_sil, color='red', linestyle='--', label=f'Max Silhouette (k={best_k_sil}: {silhouette_scores[best_k_sil]:.4f})')
    ax1.set_title("Silhouette Score vs Number of Clusters (k)", fontsize=12, fontweight='bold')
    ax1.set_xlabel("Number of Clusters (k)", fontsize=10)
    ax1.set_ylabel("Average Silhouette Coefficient", fontsize=10)
    ax1.set_xticks(list(k_range))
    ax1.legend(frameon=True, facecolor='white')

    ax2.plot(list(k_range), [inertias[k] for k in k_range], 's-', color='#ff7f0e', linewidth=2, markersize=8)
    ax2.set_title("Elbow Method: Within-Cluster Sum of Squares (Inertia)", fontsize=12, fontweight='bold')
    ax2.set_xlabel("Number of Clusters (k)", fontsize=10)
    ax2.set_ylabel("Inertia", fontsize=10)
    ax2.set_xticks(list(k_range))
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "01_k_selection_silhouette_elbow.png"), dpi=300)
    plt.close()

    # Step 3: Pick k and profile
    # Let's inspect highest silhouette vs interpretability:
    # If k=2 or k=3 yields highest, we also check both for deep interpretability.
    chosen_k = best_k_sil
    km_best, labels_best = models[chosen_k]
    df['cluster'] = labels_best

    # Also record k=3 if chosen_k != 3 for comparative depth
    alt_k = 3 if chosen_k != 3 else 2
    km_alt, labels_alt = models[alt_k]
    df[f'cluster_k{alt_k}'] = labels_alt

    # Cluster profiling for chosen_k
    profile_rows = []
    for c in range(chosen_k):
        c_mask = (df['cluster'] == c)
        c_size = c_mask.sum()
        c_pct = (c_size / len(df)) * 100
        row = {
            'Cluster': f'Cluster {c+1}',
            'Size_N': c_size,
            'Size_Pct': round(c_pct, 2)
        }
        for col in feature_cols:
            row[f'{col}_Mean'] = round(df.loc[c_mask, col].mean(), 3)
            row[f'{col}_Std'] = round(df.loc[c_mask, col].std(), 3)
        profile_rows.append(row)
    profile_df = pd.DataFrame(profile_rows)
    profile_df.to_csv(os.path.join(out_dir, f"cluster_profile_k{chosen_k}.csv"), index=False)

    # Standardised Centroids
    centroids_std = pd.DataFrame(km_best.cluster_centers_, columns=feature_cols,
                                 index=[f'Cluster {i+1}' for i in range(chosen_k)])
    centroids_std.to_csv(os.path.join(out_dir, f"centroids_standardised_k{chosen_k}.csv"))

    # Step 4: Cross-tabulation vs Station and Adjusted Rand Index (ARI)
    cross_tab = pd.crosstab(df['cluster'].map(lambda x: f'Cluster {x+1}'), df['station'], margins=True)
    cross_tab.to_csv(os.path.join(out_dir, f"crosstab_cluster_vs_station_k{chosen_k}.csv"))

    ari = adjusted_rand_score(df['station'], df['cluster'])
    ari_alt = adjusted_rand_score(df['station'], df[f'cluster_k{alt_k}'])

    # Step 5: Scatter Plots of Clusters
    fig, (ax_sc1, ax_sc2) = plt.subplots(1, 2, figsize=(14, 6))
    cluster_palette = sns.color_palette("Set2", chosen_k)

    # WSPD vs BAR
    for c in range(chosen_k):
        c_df = df[df['cluster'] == c]
        ax_sc1.scatter(c_df['BAR (hPa)'], c_df['WSPD (m s-1)'],
                       label=f'Cluster {c+1} (N={len(c_df)})', alpha=0.6, s=25, color=cluster_palette[c])
    # Plot unstandardised centroid
    for c in range(chosen_k):
        orig_mean_bar = df.loc[df['cluster'] == c, 'BAR (hPa)'].mean()
        orig_mean_wspd = df.loc[df['cluster'] == c, 'WSPD (m s-1)'].mean()
        ax_sc1.scatter(orig_mean_bar, orig_mean_wspd, color='black', marker='X', s=120, edgecolors='white', linewidth=1.5)
    ax_sc1.set_title(f"k-Means (k={chosen_k}): Barometric Pressure vs Wind Speed", fontsize=12, fontweight='bold')
    ax_sc1.set_xlabel("Barometric Pressure (hPa)", fontsize=10)
    ax_sc1.set_ylabel("Wind Speed (m/s)", fontsize=10)
    ax_sc1.legend(frameon=True, facecolor='white')

    # ATMP vs WSPD
    for c in range(chosen_k):
        c_df = df[df['cluster'] == c]
        ax_sc2.scatter(c_df['ATMP (degree_C)'], c_df['WSPD (m s-1)'],
                       label=f'Cluster {c+1} (N={len(c_df)})', alpha=0.6, s=25, color=cluster_palette[c])
    for c in range(chosen_k):
        orig_mean_atmp = df.loc[df['cluster'] == c, 'ATMP (degree_C)'].mean()
        orig_mean_wspd = df.loc[df['cluster'] == c, 'WSPD (m s-1)'].mean()
        ax_sc2.scatter(orig_mean_atmp, orig_mean_wspd, color='black', marker='X', s=120, edgecolors='white', linewidth=1.5)
    ax_sc2.set_title(f"k-Means (k={chosen_k}): Air Temperature vs Wind Speed", fontsize=12, fontweight='bold')
    ax_sc2.set_xlabel("Air Temperature (°C)", fontsize=10)
    ax_sc2.set_ylabel("Wind Speed (m/s)", fontsize=10)
    ax_sc2.legend(frameon=True, facecolor='white')

    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, f"02_cluster_scatter_k{chosen_k}.png"), dpi=300)
    plt.close()

    # Step 6: Detailed Clustering Report
    with open(os.path.join(out_dir, "clustering_report.txt"), "w", encoding="utf-8") as f:
        f.write("="*70 + "\n")
        f.write("K-MEANS CLUSTERING ANALYSIS REPORT\n")
        f.write("="*70 + "\n\n")
        f.write("1. SILHOUETTE COEFFICIENT BY K:\n")
        for k in k_range:
            f.write(f"   - k = {k}: Silhouette = {silhouette_scores[k]:.4f}, Inertia = {inertias[k]:.2f}\n")
        f.write(f"\n   Optimal k by silhouette: k = {best_k_sil} (Silhouette: {silhouette_scores[best_k_sil]:.4f})\n\n")

        f.write(f"2. CHOSEN CLUSTER MODEL: k = {chosen_k}\n")
        for idx, row in profile_df.iterrows():
            f.write(f"   - {row['Cluster']} (N = {row['Size_N']}, {row['Size_Pct']}%):\n")
            f.write(f"     * Wind Speed: {row['WSPD (m s-1)_Mean']} ± {row['WSPD (m s-1)_Std']} m/s\n")
            f.write(f"     * Wind Gust:  {row['GST (m s-1)_Mean']} ± {row['GST (m s-1)_Std']} m/s\n")
            f.write(f"     * Pressure:   {row['BAR (hPa)_Mean']} ± {row['BAR (hPa)_Std']} hPa\n")
            f.write(f"     * Air Temp:   {row['ATMP (degree_C)_Mean']} ± {row['ATMP (degree_C)_Std']} °C\n")

        f.write(f"\n3. CROSS-TABULATION VS BUOY STATION:\n")
        f.write(str(cross_tab) + "\n\n")

        f.write(f"4. ADJUSTED RAND INDEX (ARI) EVALUATION:\n")
        f.write(f"   - Adjusted Rand Index vs Station (k={chosen_k}): {ari:.4f}\n")
        f.write(f"   - Adjusted Rand Index vs Station (k={alt_k}): {ari_alt:.4f}\n")
        f.write(f"   - Interpretation:\n")
        if abs(ari) < 0.3:
            f.write(f"     The low ARI value ({ari:.4f}) confirms that the unsupervised k-Means clusters\n")
            f.write(f"     DO NOT merely replicate the geographic buoy stations. Instead, they represent\n")
            f.write(f"     distinct, cross-station meteorological regimes (e.g. calm warm conditions vs\n")
            f.write(f"     disturbed windy high-seas conditions) that occur at both geographic locations.\n")
        else:
            f.write(f"     The moderate/high ARI value ({ari:.4f}) indicates partial geographic stratification\n")
            f.write(f"     in cluster assignment, reflecting regional climate differences.\n")

        f.write(f"\n5. NEUTRAL METEOROLOGICAL CHARACTERIZATION (Academic Safety Notice):\n")
        f.write(f"   Per project guidelines, clusters are described strictly by physical measurements,\n")
        f.write(f"   NOT as 'safe/dangerous' and NOT as Potential Fishing Zones (PFZs):\n")
        for c in range(chosen_k):
            w = profile_df.loc[c, 'WSPD (m s-1)_Mean']
            b = profile_df.loc[c, 'BAR (hPa)_Mean']
            t = profile_df.loc[c, 'ATMP (degree_C)_Mean']
            f.write(f"   - Cluster {c+1}: Characterized by mean wind speed of {w:.2f} m/s, barometric pressure of {b:.2f} hPa, and air temperature of {t:.2f} °C.\n")

    # Save labeled clustered dataset
    df.to_csv(os.path.join(out_dir, "cleaned_with_clusters.csv"), index=False)
    print(f"Clustering complete! Outputs saved to {out_dir}")

if __name__ == "__main__":
    run_clustering()
