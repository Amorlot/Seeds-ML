import os
from flask import Blueprint, jsonify, send_file
from lib.api.state import config

plots_bp = Blueprint("plots", __name__, url_prefix="/plots")


def _plots_dir() -> str:
    return config["output"]["plots_dir"]


@plots_bp.route("/", methods=["GET"])
def list_plots():
    """Lista tutti i plot disponibili."""
    if not os.path.isdir(_plots_dir()):
        return jsonify([])
    files = [f for f in os.listdir(_plots_dir()) if f.endswith(".png")]
    return jsonify(sorted(files))


@plots_bp.route("/<filename>", methods=["GET"])
def get_plot(filename):
    """Restituisce un plot PNG per nome file."""
    if not filename.endswith(".png"):
        return jsonify({"error": "Solo file .png supportati"}), 400
    path = os.path.join(_plots_dir(), filename)
    if not os.path.isfile(path):
        return jsonify({"error": f"Plot '{filename}' non trovato"}), 404
    return send_file(os.path.abspath(path), mimetype="image/png")
