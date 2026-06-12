from flask import Blueprint, request, jsonify
from lib.loader import GenericLoader
from lib.api.state import pipeline

loader_bp = Blueprint("loader", __name__, url_prefix="/loader")


@loader_bp.route("/load", methods=["POST"])
def load():
    """
    Carica il dataset da UCI o CSV e salva loader + y nello stato.

    Body JSON:
      - dataset_id  (int)  oppure
      - csv_path    (str)
      - target_col  (str, obbligatorio)
    """
    body = request.get_json() or {}

    if "target_col" not in body:
        return jsonify({"error": "target_col è obbligatorio"}), 400
    if "dataset_id" not in body and "csv_path" not in body:
        return jsonify({"error": "Specificare dataset_id oppure csv_path"}), 400

    loader = GenericLoader(
        target_col=body["target_col"],
        dataset_id=body.get("dataset_id"),
        csv_path=body.get("csv_path"),
    )
    loader.load()

    pipeline["loader"] = loader
    pipeline["y"] = loader.df[body["target_col"]].values

    return jsonify({"status": "ok", **loader.info()})


@loader_bp.route("/info", methods=["GET"])
def info():
    """Restituisce informazioni sul dataset caricato."""
    loader = pipeline["loader"]
    if loader is None:
        return jsonify({"error": "Dataset non caricato. Chiamare prima POST /loader/load"}), 400
    return jsonify(loader.info())


@loader_bp.route("/missing", methods=["GET"])
def missing():
    """Report dei valori mancanti per colonna."""
    loader = pipeline["loader"]
    if loader is None:
        return jsonify({"error": "Dataset non caricato. Chiamare prima POST /loader/load"}), 400
    return jsonify(loader.missing_report())
