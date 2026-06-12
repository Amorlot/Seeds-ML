import os

import numpy as np
import yaml

from lib.cleaner import GenericCleaner
from lib.eda import GenericEda
from lib.encoder import GenericEncoder
from lib.kmeans import KMeansModel
from lib.loader import GenericLoader
from lib.plots import KMeansPlotter

SEP = "=" * 65


def section(title: str) -> None:
    print(f"\n{SEP}\n  {title}\n{SEP}")


def load_config(path: str = "config.yaml") -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def main():
    cfg = load_config()
    plots_dir = cfg["output"]["plots_dir"]
    os.makedirs(plots_dir, exist_ok=True)

    # ── CARICAMENTO DATI ─────────────────────────────────────────
    section("CARICAMENTO DATI")
    loader = GenericLoader(
        target_col=cfg["loader"]["target_col"],
        dataset_id=cfg["loader"].get("dataset_id"),
        csv_path=cfg["loader"].get("csv_path"),
        col_names=cfg["loader"].get("col_names"),
    )
    loader.load()
    info = loader.info()
    print(f"  Righe:       {info['rows']}")
    print(f"  Feature num: {info['numerical']}")
    print(f"  Feature cat: {info['categorical']}")
    print(f"  Distribuzione target (classi reali):")
    for cls, cnt in sorted(info["target_distribution"].items()):
        print(f"    classe {cls}: {cnt} campioni")

    miss = loader.missing_report()
    if miss:
        print("  Valori mancanti:")
        for col, v in miss.items():
            print(f"    {col}: {v['count']} ({v['pct']}%)")
    else:
        print("  Nessun valore mancante.")

    target_col = cfg["loader"]["target_col"]
    X_raw = loader.df.drop(columns=[target_col])
    y = loader.df[target_col].values

    # ── EDA ──────────────────────────────────────────────────────
    section("EDA — ANALISI ESPLORATIVA")
    eda = GenericEda(X_raw)
    summ = eda.summary()
    if "numerical" in summ:
        print(f"  {'Feature':<22}  {'mean':>9}  {'std':>9}  {'min':>9}  {'max':>9}")
        print("  " + "-" * 60)
        for feat, stats in summ["numerical"].items():
            print(
                f"  {feat:<22}  {stats.get('mean', 0):>9.4f}"
                f"  {stats.get('std', 0):>9.4f}"
                f"  {stats.get('min', 0):>9.4f}"
                f"  {stats.get('max', 0):>9.4f}"
            )

    corr = eda.correlation()
    if corr:
        print("\n  Coppie altamente correlate (|r| > 0.85):")
        shown = set()
        found = False
        for col_a, row in corr.items():
            for col_b, val in row.items():
                if col_a != col_b and val is not None and abs(val) > 0.85:
                    pair = tuple(sorted([col_a, col_b]))
                    if pair not in shown:
                        shown.add(pair)
                        print(f"    {col_a} ↔ {col_b}: {val:.4f}")
                        found = True
        if not found:
            print("    nessuna coppia con |r| > 0.85")

    # ── PULIZIA ──────────────────────────────────────────────────
    section("PULIZIA DATI")
    cleaner = GenericCleaner()
    cleaner.configure(
        num_strategy=cfg["cleaner"]["num_strategy"],
        cat_strategy=cfg["cleaner"].get("cat_strategy", "unknown"),
    )
    X_clean = cleaner.fit_transform(X_raw)
    print(f"  Shape: {X_clean.shape}")
    print(f"  Valori mancanti residui: {int(X_clean.isnull().sum().sum())}")

    # ── SCALING ──────────────────────────────────────────────────
    section("SCALING FEATURES")
    encoder = GenericEncoder()
    encoder.configure(
        num_strategy=cfg["encoder"]["num_strategy"],
        cat_strategy="ohe",
    )
    X_scaled_df = encoder.fit_transform_features(X_clean)
    X_scaled = X_scaled_df.values
    print(f"  Shape dopo scaling: {X_scaled.shape}")
    print(f"  Strategia: {cfg['encoder']['num_strategy']}")

    # ── RICERCA K ────────────────────────────────────────────────
    section("RICERCA K — ELBOW + SILHOUETTE")
    km_cfg = cfg["kmeans"]
    km = KMeansModel()
    plotter = KMeansPlotter()
    search_results = km.search(
        X_scaled,
        k_min=km_cfg["k_min"],
        k_max=km_cfg["k_max"],
        random_state=km_cfg["random_state"],
        n_init=km_cfg["n_init"],
    )

    print(f"  {'k':>4}  {'Inertia':>12}  {'Silhouette':>12}")
    print("  " + "-" * 34)
    for k, v in sorted(search_results.items()):
        print(f"  {k:>4}  {v['inertia']:>12.2f}  {v['silhouette']:>12.4f}")

    best_k: int = km_cfg.get("best_k") or km.best_k_by_silhouette(search_results)
    print(f"\n  Miglior k selezionato: {best_k}  (silhouette={search_results[best_k]['silhouette']:.4f})")

    plot_path = plotter.elbow_silhouette(search_results, plots_dir)
    print(f"  [plot] {plot_path}")

    # ── CLUSTERING FIT ───────────────────────────────────────────
    section(f"CLUSTERING FIT  (k={best_k})")
    km.fit(
        X_scaled,
        best_k,
        random_state=km_cfg["random_state"],
        n_init=km_cfg["n_init"],
    )
    sizes = km.cluster_sizes()
    print(f"  Inertia:    {km.inertia():.4f}")
    print(f"  Silhouette: {km.silhouette(X_scaled):.4f}")
    print(f"  Dimensioni cluster:")
    for c, n in sizes.items():
        pct = n / len(X_scaled) * 100
        print(f"    cluster {c}: {n:>4} campioni  ({pct:.1f}%)")

    # ── PROFILI CLUSTER ──────────────────────────────────────────
    section("PROFILI CLUSTER  (scala originale)")
    profiles = km.cluster_profiles(X_clean)
    print(profiles.to_string())

    plot_path = plotter.profiles(profiles, plots_dir)
    print(f"\n  [plot] {plot_path}")

    # ── CONFRONTO CON ETICHETTE REALI ───────────────────────────
    section("CONFRONTO CON ETICHETTE REALI")
    comparison = km.compare_labels(y)
    print(f"  Adjusted Rand Index (ARI): {comparison['ari']:>7}  (range [-1, 1], 1=perfetto)")
    print(f"  Normalized Mutual Info (NMI): {comparison['nmi']:>7}  (range  [0, 1], 1=perfetto)")
    print(f"  Purity:                    {comparison['purity']:>7}  (range  [0, 1], 1=perfetto)")

    # ── VISUALIZZAZIONI ──────────────────────────────────────────
    section("VISUALIZZAZIONI")
    plot_path = plotter.pca2d(X_scaled, km.labels_, km.k, y_true=y, save_dir=plots_dir)
    print(f"  [plot] {plot_path}")

    plot_path = plotter.pairplot(X_clean, km.labels_, save_dir=plots_dir)
    print(f"  [plot] {plot_path}")

    # ── RIEPILOGO ────────────────────────────────────────────────
    section("RIEPILOGO FINALE")
    src = cfg["loader"].get("csv_path") or f"UCI id={cfg['loader'].get('dataset_id')}"
    print(f"  Dataset:      {src} — {X_scaled.shape[0]} campioni, {X_scaled.shape[1]} feature")
    print(f"  Scaling:      {cfg['encoder']['num_strategy']}")
    print(f"  k ricercato:  {km_cfg['k_min']}..{km_cfg['k_max']}")
    print(f"  Miglior k:    {best_k}")
    print(f"  Inertia:      {km.inertia():.4f}")
    print(f"  Silhouette:   {km.silhouette(X_scaled):.4f}")
    print(f"  ARI:          {comparison['ari']}")
    print(f"  NMI:          {comparison['nmi']}")
    print(f"  Purity:       {comparison['purity']}")
    print(f"  Plot in:      {plots_dir}")
    print(f"\n{SEP}\n  FINE\n{SEP}\n")


if __name__ == "__main__":
    main()
