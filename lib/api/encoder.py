from flask import Blueprint, request, jsonify
from lib.encoder import GenericEncoder
from lib.api.state import pipeline

encoder_bp = Blueprint("encoder", __name__, url_prefix="/encoder")


@encoder_bp.route("/configure", methods=["POST"])
def configure():
    """
    Configura la strategia di scaling.

    Body JSON (opzionale):
      - num_strategy : 'standard' | 'minmax' | 'none'  (default: 'standard')
    """
    if pipeline["X_clean"] is None:
        return jsonify({"error": "Chiamare prima POST /cleaner/fit_transform"}), 400

    body = request.get_json() or {}
    encoder = GenericEncoder()
    encoder.configure(
        num_strategy=body.get("num_strategy", "standard"),
        cat_strategy="ohe",
    )
    pipeline["encoder"] = encoder
    return jsonify({"status": "configured", "num_strategy": body.get("num_strategy", "standard")})


@encoder_bp.route("/fit_transform", methods=["POST"])
def fit_transform():
    """Scala le feature e salva X_scaled nello stato."""
    encoder = pipeline["encoder"]
    X_clean = pipeline["X_clean"]
    if encoder is None:
        return jsonify({"error": "Chiamare prima POST /encoder/configure"}), 400

    X_scaled_df = encoder.fit_transform_features(X_clean)
    pipeline["X_scaled"] = X_scaled_df.values
    return jsonify({
        "status": "ok",
        "shape": list(pipeline["X_scaled"].shape),
    })
