from flask import Blueprint, request, jsonify
from lib.kmeans import KMeansModel
from lib.plots import KMeansPlotter
from lib.api.state import pipeline, config

kmeans_bp = Blueprint("kmeans", __name__, url_prefix="/kmeans")

_PLOTS_DIR = "output/"
_plotter = KMeansPlotter()


def _require_scaled():
    if pipeline["X_scaled"] is None:
        return jsonify({"error": "Chiamare prima POST /encoder/fit_transform"}), 400
    return None


def _require_fit():
    if pipeline["km"] is None or pipeline["km"].labels_ is None:
        return jsonify({"error": "Chiamare prima POST /kmeans/fit"}), 400
    return None


# ── Ricerca K ─────────────────────────────────────────────────────────────────

@kmeans_bp.route("/search", methods=["POST"])
def search():
    """
    Calcola inertia e silhouette per k in [k_min, k_max].

    Body JSON (tutti opzionali):
      - k_min        : int  (default: 2)
      - k_max        : int  (default: 10)
      - random_state : int  (default: 42)
      - n_init       : int  (default: 10)
    """
    err = _require_scaled()
    if err:
        return err

    body = request.get_json() or {}
    km = pipeline["km"] or KMeansModel()
    pipeline["km"] = km

    if pipeline["X_scaled"] is None:
        return jsonify({"error": "Dati non disponibili"}), 400

    cfg = config["kmeans"]
    results = km.search(
        pipeline["X_scaled"],
        k_min=body.get("k_min", cfg["k_min"]),
        k_max=body.get("k_max", cfg["k_max"]),
        random_state=body.get("random_state", cfg["random_state"]),
        n_init=body.get("n_init", cfg["n_init"]),
    )
    pipeline["search_results"] = results
    best_k = km.best_k_by_silhouette(results)

    return jsonify({
        "status": "ok",
        "best_k_silhouette": best_k,
        "results": {str(k): v for k, v in results.items()},
    })


@kmeans_bp.route("/search_results", methods=["GET"])
def search_results():
    """Restituisce i risultati dell'ultima ricerca."""
    if pipeline["search_results"] is None:
        return jsonify({"error": "Chiamare prima POST /kmeans/search"}), 400
    results = pipeline["search_results"]
    best_k = pipeline["km"].best_k_by_silhouette(results)
    return jsonify({
        "best_k_silhouette": best_k,
        "results": {str(k): v for k, v in results.items()},
    })


# ── Fitting ───────────────────────────────────────────────────────────────────

@kmeans_bp.route("/fit", methods=["POST"])
def fit():
    """
    Addestra K-Means con il k scelto.

    Body JSON (opzionali):
      - k            : int  (default: auto da silhouette)
      - random_state : int  (default: 42)
      - n_init       : int  (default: 10)
    """
    err = _require_scaled()
    if err:
        return err

    body = request.get_json() or {}
    km = pipeline["km"] or KMeansModel()
    pipeline["km"] = km

    if "k" in body:
        k = int(body["k"])
    elif pipeline["search_results"]:
        k = km.best_k_by_silhouette(pipeline["search_results"])
    else:
        return jsonify({"error": "Specificare k oppure eseguire prima POST /kmeans/search"}), 400

    cfg = config["kmeans"]
    km.fit(
        pipeline["X_scaled"],
        k,
        random_state=body.get("random_state", cfg["random_state"]),
        n_init=body.get("n_init", cfg["n_init"]),
    )

    return jsonify({
        "status": "ok",
        "k": k,
        "inertia": km.inertia(),
        "silhouette": km.silhouette(pipeline["X_scaled"]),
        "cluster_sizes": km.cluster_sizes(),
    })


# ── Analisi post-fit ──────────────────────────────────────────────────────────

@kmeans_bp.route("/cluster_sizes", methods=["GET"])
def cluster_sizes():
    """Numero di campioni per cluster."""
    err = _require_fit()
    if err:
        return err
    return jsonify(pipeline["km"].cluster_sizes())


@kmeans_bp.route("/profiles", methods=["GET"])
def profiles():
    """Media delle feature per cluster (scala originale)."""
    err = _require_fit()
    if err:
        return err
    if pipeline["X_clean"] is None:
        return jsonify({"error": "X_clean non disponibile"}), 400
    prof = pipeline["km"].cluster_profiles(pipeline["X_clean"])
    return jsonify(prof.to_dict())


@kmeans_bp.route("/compare", methods=["GET"])
def compare():
    """Confronto cluster vs etichette reali: ARI, NMI, purity."""
    err = _require_fit()
    if err:
        return err
    if pipeline["y"] is None:
        return jsonify({"error": "Etichette reali non disponibili"}), 400
    return jsonify(pipeline["km"].compare_labels(pipeline["y"]))


# ── Plot ─────────────────────────────────────────────────────────────────────

@kmeans_bp.route("/plot/elbow", methods=["POST"])
def plot_elbow():
    """Genera e salva il grafico elbow + silhouette."""
    if pipeline["search_results"] is None:
        return jsonify({"error": "Chiamare prima POST /kmeans/search"}), 400
    path = _plotter.elbow_silhouette(pipeline["search_results"], _PLOTS_DIR)
    return jsonify({"status": "ok", "path": path})


@kmeans_bp.route("/plot/pca2d", methods=["POST"])
def plot_pca2d():
    """Genera e salva lo scatter PCA 2D (cluster + classi reali se disponibili)."""
    err = _require_fit()
    if err:
        return err
    km = pipeline["km"]
    path = _plotter.pca2d(
        pipeline["X_scaled"],
        km.labels_,
        km.k,
        y_true=pipeline["y"],
        save_dir=_PLOTS_DIR,
    )
    return jsonify({"status": "ok", "path": path})


@kmeans_bp.route("/plot/profiles", methods=["POST"])
def plot_profiles():
    """Genera e salva la heatmap dei profili cluster."""
    err = _require_fit()
    if err:
        return err
    if pipeline["X_clean"] is None:
        return jsonify({"error": "X_clean non disponibile"}), 400
    prof = pipeline["km"].cluster_profiles(pipeline["X_clean"])
    path = _plotter.profiles(prof, _PLOTS_DIR)
    return jsonify({"status": "ok", "path": path})


@kmeans_bp.route("/plot/pairplot", methods=["POST"])
def plot_pairplot():
    """Genera e salva il pairplot delle feature colorate per cluster."""
    err = _require_fit()
    if err:
        return err
    if pipeline["X_clean"] is None:
        return jsonify({"error": "X_clean non disponibile"}), 400
    path = _plotter.pairplot(pipeline["X_clean"], pipeline["km"].labels_, _PLOTS_DIR)
    return jsonify({"status": "ok", "path": path})
