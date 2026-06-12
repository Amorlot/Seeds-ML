import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import (
    adjusted_rand_score,
    normalized_mutual_info_score,
    silhouette_score,
)


class KMeansModel:
    """
    K-Means per unsupervised pattern discovery su dati numerici.

    Workflow:
      1. search()  — elbow + silhouette per k in [k_min, k_max]
      2. fit()     — addestra con il k scelto
      3. cluster_profiles() / compare_labels()
    """

    def __init__(self):
        self.model: KMeans = None
        self.k: int = None
        self.labels_: np.ndarray = None

    # ── Ricerca K ─────────────────────────────────────────────────────────────

    def search(
        self,
        X: np.ndarray,
        k_min: int = 2,
        k_max: int = 10,
        random_state: int = 42,
        n_init: int = 10,
    ) -> dict:
        """Calcola inertia e silhouette per ogni k in [k_min, k_max]."""
        results = {}
        for k in range(k_min, k_max + 1):
            km = KMeans(n_clusters=k, random_state=random_state, n_init=n_init)
            labels = km.fit_predict(X)
            sil = float(silhouette_score(X, labels))
            results[k] = {"inertia": float(km.inertia_), "silhouette": sil}
        return results

    def best_k_by_silhouette(self, search_results: dict) -> int:
        return max(search_results.items(), key=lambda kv: kv[1]["silhouette"])[0]

    # ── Fitting ───────────────────────────────────────────────────────────────

    def fit(
        self,
        X: np.ndarray,
        k: int,
        random_state: int = 42,
        n_init: int = 10,
    ) -> "KMeansModel":
        self.k = k
        self.model = KMeans(n_clusters=k, random_state=random_state, n_init=n_init)
        self.labels_ = self.model.fit_predict(X)
        return self

    # ── Metriche ──────────────────────────────────────────────────────────────

    def inertia(self) -> float:
        return float(self.model.inertia_)

    def silhouette(self, X: np.ndarray) -> float:
        return float(silhouette_score(X, self.labels_))

    def cluster_sizes(self) -> dict:
        unique, counts = np.unique(self.labels_, return_counts=True)
        return {int(c): int(n) for c, n in zip(unique, counts)}

    def cluster_profiles(self, X_orig: pd.DataFrame) -> pd.DataFrame:
        """Media di ogni feature per cluster (spazio originale, non scalato)."""
        df = X_orig.copy()
        df["_cluster"] = self.labels_
        return df.groupby("_cluster").mean(numeric_only=True).round(4)

    def compare_labels(self, y_true) -> dict:
        """Confronto cluster vs etichette reali: ARI, NMI, purity."""
        y_arr = np.array(y_true)
        ari = adjusted_rand_score(y_arr, self.labels_)
        nmi = normalized_mutual_info_score(y_arr, self.labels_)
        purity = self._purity(y_arr, self.labels_)
        return {
            "ari": round(float(ari), 4),
            "nmi": round(float(nmi), 4),
            "purity": round(float(purity), 4),
        }

    @staticmethod
    def _purity(y_true: np.ndarray, labels: np.ndarray) -> float:
        total = len(y_true)
        purity_sum = 0
        for c in np.unique(labels):
            mask = labels == c
            _, counts = np.unique(y_true[mask], return_counts=True)
            purity_sum += counts.max()
        return purity_sum / total
