import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.decomposition import PCA


class KMeansPlotter:
    """Visualizzazioni per risultati K-Means. Separata dalla logica di clustering."""

    def elbow_silhouette(self, search_results: dict, save_dir: str) -> str:
        """Grafico elbow (inertia) + silhouette score per ogni k."""
        os.makedirs(save_dir, exist_ok=True)
        ks = sorted(search_results)
        inertias = [search_results[k]["inertia"] for k in ks]
        silhouettes = [search_results[k]["silhouette"] for k in ks]
        best_k = max(zip(ks, silhouettes), key=lambda x: x[1])[0]

        fig, axes = plt.subplots(1, 2, figsize=(12, 4))

        axes[0].plot(ks, inertias, "o-", color="steelblue", linewidth=2)
        axes[0].set_title("Elbow — Inertia vs k")
        axes[0].set_xlabel("k")
        axes[0].set_ylabel("Inertia")
        axes[0].grid(alpha=0.3)

        axes[1].plot(ks, silhouettes, "o-", color="darkorange", linewidth=2)
        axes[1].axvline(best_k, color="red", linestyle="--", alpha=0.6, label=f"best k={best_k}")
        axes[1].set_title("Silhouette Score vs k")
        axes[1].set_xlabel("k")
        axes[1].set_ylabel("Silhouette")
        axes[1].legend()
        axes[1].grid(alpha=0.3)

        plt.tight_layout()
        path = os.path.join(save_dir, "elbow_silhouette.png")
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()
        return path

    def pca2d(
        self,
        X_scaled: np.ndarray,
        labels: np.ndarray,
        k: int,
        y_true=None,
        save_dir: str = "output/",
    ) -> str:
        """Scatter PCA 2D: cluster assegnati (sinistra) vs classi reali (destra)."""
        os.makedirs(save_dir, exist_ok=True)
        pca = PCA(n_components=2, random_state=42)
        coords = pca.fit_transform(X_scaled)
        var = pca.explained_variance_ratio_

        ncols = 2 if y_true is not None else 1
        fig, axes = plt.subplots(1, ncols, figsize=(6 * ncols, 5))
        if ncols == 1:
            axes = [axes]

        sc = axes[0].scatter(
            coords[:, 0], coords[:, 1],
            c=labels, cmap="tab10", s=40, alpha=0.85,
        )
        axes[0].set_title(f"K-Means (k={k}) — Cluster assegnati")
        axes[0].set_xlabel(f"PC1 ({var[0] * 100:.1f}%)")
        axes[0].set_ylabel(f"PC2 ({var[1] * 100:.1f}%)")
        plt.colorbar(sc, ax=axes[0], label="Cluster")

        if y_true is not None:
            y_arr = np.array(y_true)
            sc2 = axes[1].scatter(
                coords[:, 0], coords[:, 1],
                c=y_arr, cmap="Set1", s=40, alpha=0.85,
            )
            axes[1].set_title("Classi Reali (ground truth)")
            axes[1].set_xlabel(f"PC1 ({var[0] * 100:.1f}%)")
            axes[1].set_ylabel(f"PC2 ({var[1] * 100:.1f}%)")
            plt.colorbar(sc2, ax=axes[1], label="Classe")

        plt.tight_layout()
        path = os.path.join(save_dir, "pca2d.png")
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()
        return path

    def profiles(self, profiles_df: pd.DataFrame, save_dir: str = "output/") -> str:
        """Heatmap delle medie delle feature per ogni cluster."""
        os.makedirs(save_dir, exist_ok=True)
        w = max(8, len(profiles_df.columns) * 1.2)
        fig, ax = plt.subplots(figsize=(w, 4))
        sns.heatmap(
            profiles_df.T,
            annot=True,
            fmt=".2f",
            cmap="YlOrRd",
            ax=ax,
            linewidths=0.5,
            linecolor="white",
        )
        ax.set_title("Profili Cluster — media feature (scala originale)")
        ax.set_xlabel("Cluster")
        ax.set_ylabel("Feature")
        plt.tight_layout()
        path = os.path.join(save_dir, "cluster_profiles.png")
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()
        return path

    def pairplot(
        self,
        X_orig: pd.DataFrame,
        labels: np.ndarray,
        save_dir: str = "output/",
    ) -> str:
        """Pairplot delle feature originali colorate per cluster."""
        os.makedirs(save_dir, exist_ok=True)
        df = X_orig.copy()
        df["Cluster"] = labels.astype(str)
        g = sns.pairplot(df, hue="Cluster", diag_kind="kde", plot_kws={"alpha": 0.5})
        g.figure.suptitle("Pairplot Feature — colorate per Cluster", y=1.02)
        path = os.path.join(save_dir, "pairplot.png")
        g.figure.savefig(path, dpi=120, bbox_inches="tight")
        plt.close("all")
        return path
