import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import (
    adjusted_rand_score,
    normalized_mutual_info_score,
    silhouette_score,
)

_KMEDOIDS_METRICS = {"manhattan", "cosine", "chebyshev", "minkowski"}


def _build_model(k: int, metric: str, random_state: int, n_init: int):
    """Factory: sceglie il backend in base alla metrica."""
    if metric == "euclidean":
        return KMeans(n_clusters=k, random_state=random_state, n_init=n_init)
    elif metric in _KMEDOIDS_METRICS or metric == "gower":
        from sklearn_extra.cluster import KMedoids
        m = "precomputed" if metric == "gower" else metric
        return KMedoids(n_clusters=k, metric=m, random_state=random_state)
    elif metric == "hamming":
        from kmodes.kmodes import KModes
        return KModes(n_clusters=k, random_state=random_state, n_init=n_init)
    else:
        raise ValueError(
            f"Metrica non supportata: '{metric}'. "
            "Usa: euclidean, manhattan, cosine, gower, hamming"
        )


def _to_input(X, metric: str):
    """Converte X nella forma attesa dall'algoritmo (matrice di distanze per gower)."""
    if metric == "gower":
        import gower
        return gower.gower_matrix(X)
    return X


def _sil_metric(metric: str) -> str:
    return "precomputed" if metric == "gower" else metric


def _get_inertia(model) -> float:
    """Inertia per KMeans/KMedoids, cost per KModes."""
    return float(getattr(model, "inertia_", getattr(model, "cost_", 0.0)))


class KMeansModel:
    """
    Clustering generico: KMeans (euclidean), KMedoids (manhattan/cosine/gower),
    KModes (hamming).

    Workflow:
      1. search()  — elbow + silhouette per k in [k_min, k_max]
      2. fit()     — addestra con il k scelto
      3. cluster_profiles() / compare_labels()
    """

    def __init__(self):
        self.model = None
        self.k: int = None
        self.labels_: np.ndarray = None
        self.metric: str = "euclidean"
        self._dist_matrix: np.ndarray = None  # cache per gower

    # ── Ricerca K ─────────────────────────────────────────────────────────────

    def search(
        self,
        X,
        k_min: int = 2,
        k_max: int = 10,
        random_state: int = 42,
        n_init: int = 10,
        metric: str = "euclidean",
    ) -> dict:
        """Calcola inertia e silhouette per ogni k in [k_min, k_max]."""
        self.metric = metric
        X_in = _to_input(X, metric)
        if metric == "gower":
            self._dist_matrix = X_in

        results = {}
        for k in range(k_min, k_max + 1):
            model = _build_model(k, metric, random_state, n_init)
            labels = model.fit_predict(X_in)
            sil = float(silhouette_score(X_in, labels, metric=_sil_metric(metric)))
            results[k] = {"inertia": _get_inertia(model), "silhouette": sil}
        return results

    def best_k_by_silhouette(self, search_results: dict) -> int:
        return max(search_results.items(), key=lambda kv: kv[1]["silhouette"])[0]

    # ── Fitting ───────────────────────────────────────────────────────────────

    def fit(
        self,
        X,
        k: int,
        random_state: int = 42,
        n_init: int = 10,
        metric: str = "euclidean",
    ) -> "KMeansModel":
        self.k = k
        self.metric = metric
        X_in = _to_input(X, metric)
        if metric == "gower":
            self._dist_matrix = X_in
        self.model = _build_model(k, metric, random_state, n_init)
        self.labels_ = self.model.fit_predict(X_in)
        return self

    # ── Metriche ──────────────────────────────────────────────────────────────

    def inertia(self) -> float:
        return _get_inertia(self.model)

    def silhouette(self, X) -> float:
        X_in = self._dist_matrix if self.metric == "gower" else X
        return float(silhouette_score(X_in, self.labels_, metric=_sil_metric(self.metric)))

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
