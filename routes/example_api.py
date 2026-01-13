from flask import Blueprint, jsonify
import requests
example_bp = Blueprint("example_api", __name__)
@example_bp.route("/example-api")
def example_api():
    try:
        response = requests.get("https://api.agify.io/?name=lionel")
        return jsonify({"success": True, "data": response.json()})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
