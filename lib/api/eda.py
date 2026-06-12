from flask import Blueprint, jsonify
from lib.eda import GenericEda
from lib.api.state import pipeline

eda_bp = Blueprint("eda", __name__, url_prefix="/eda")


def _get_X():
    loader = pipeline["loader"]
    if loader is None:
        return None, jsonify({"error": "Dataset non caricato. Chiamare prima POST /loader/load"}), 400
    X = loader.df.drop(columns=[loader.target_col])
    return X, None, None


@eda_bp.route("/summary", methods=["GET"])
def summary():
    """Statistiche descrittive per ogni feature numerica e categoriale."""
    X, err, code = _get_X()
    if err:
        return err, code
    return jsonify(GenericEda(X).summary())


@eda_bp.route("/missing", methods=["GET"])
def missing():
    """Valori mancanti per colonna."""
    X, err, code = _get_X()
    if err:
        return err, code
    return jsonify(GenericEda(X).missing_report())


@eda_bp.route("/correlation", methods=["GET"])
def correlation():
    """Matrice di correlazione tra feature numeriche."""
    X, err, code = _get_X()
    if err:
        return err, code
    return jsonify(GenericEda(X).correlation())
