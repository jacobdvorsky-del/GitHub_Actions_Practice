from flask import Blueprint, jsonify, request

bp = Blueprint("api", __name__)

@bp.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200