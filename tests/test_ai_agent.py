from routes.ai_agent import ai_bp
from flask import Flask
import json
def test_unauthorized():
    app = Flask(__name__); app.register_blueprint(ai_bp)
    client = app.test_client()
    response = client.post("/ask", headers={"X-API-KEY":"wrong"}, data=json.dumps({"question":"Hello"}), content_type='application/json')
    assert response.status_code == 401
