from flask import Blueprint, request, jsonify
from lib.cleaner import GenericCleaner
from lib.api.state import pipeline

cleaner_bp = Blueprint("cleaner", __name__, url_prefix="/cleaner")


@cleaner_bp.route("/configure", methods=["POST"])
def configure():
    """
    Configura le strategie di pulizia.

    Body JSON (tutti opzionali):
      - num_strategy  : 'median' | 'mean' | 'most_frequent'  (default: 'median')
      - cat_strategy  : 'unknown' | 'most_frequent'          (default: 'unknown')
    """
    if pipeline["loader"] is None:
        return jsonify({"error": "Dataset non caricato. Chiamare prima POST /loader/load"}), 400

    body = request.get_json() or {}
    cleaner = GenericCleaner()
    cleaner.configure(
        num_strategy=body.get("num_strategy", "median"),
        cat_strategy=body.get("cat_strategy", "unknown"),
    )
    pipeline["cleaner"] = cleaner
    return jsonify({"status": "configured", "num_strategy": body.get("num_strategy", "median")})


@cleaner_bp.route("/fit_transform", methods=["POST"])
def fit_transform():
    """Applica fit_transform sulle feature. Salva X_clean nello stato."""
    cleaner = pipeline["cleaner"]
    loader = pipeline["loader"]
    if cleaner is None:
        return jsonify({"error": "Chiamare prima POST /cleaner/configure"}), 400

    X = loader.df.drop(columns=[loader.target_col])
    pipeline["X_clean"] = cleaner.fit_transform(X)
    return jsonify({
        "status": "ok",
        "shape": list(pipeline["X_clean"].shape),
        "missing_residui": int(pipeline["X_clean"].isnull().sum().sum()),
    })


@cleaner_bp.route("/report", methods=["GET"])
def report():
    """Valori mancanti residui dopo la pulizia."""
    X_clean = pipeline["X_clean"]
    if X_clean is None:
        return jsonify({"error": "Chiamare prima POST /cleaner/fit_transform"}), 400
    cleaner = pipeline["cleaner"] or GenericCleaner()
    return jsonify(cleaner.report(X_clean))
