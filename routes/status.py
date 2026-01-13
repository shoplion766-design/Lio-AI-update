from flask import Blueprint, jsonify
status_bp = Blueprint("status", __name__)
@status_bp.route("/status")
def status():
    return jsonify({"status": "online", "message": "AI-Agent Copilot is active"})
