#!/bin/bash
set -e

echo "🚀 Initialisation de Lio-AI (agent IA sans bug, modulaire, testable)"

PROJECT="Lio-AI"

mkdir -p $PROJECT
cd $PROJECT

echo "📁 Création de la structure..."
mkdir -p routes plugins rag memory auto_refactor dashboard/templates tests data utils

# ---------------- ENV ----------------
cat <<EOF > .env
OPENAI_API_KEY=change_me
AGENT_API_KEY=lio-secret-key
EOF

# ---------------- REQUIREMENTS ----------------
cat <<EOF > requirements.txt
flask
requests
numpy
python-dotenv
pytest
gunicorn
EOF

# ---------------- APP ----------------
cat <<EOF > app.py
from flask import Flask
from routes.status import status_bp
from routes.ai_agent import ai_bp

app = Flask(__name__)
app.register_blueprint(status_bp)
app.register_blueprint(ai_bp)

@app.route("/")
def home():
    return "Lio-AI is running"

if __name__ == "__main__":
    app.run(debug=True)
EOF

# ---------------- STATUS ROUTE ----------------
cat <<EOF > routes/status.py
from flask import Blueprint, jsonify

status_bp = Blueprint("status", __name__)

@status_bp.route("/status")
def status():
    return jsonify({"status": "online", "agent": "Lio-AI"})
EOF

# ---------------- AI AGENT ----------------
cat <<EOF > routes/ai_agent.py
from flask import Blueprint, request, jsonify
import os

ai_bp = Blueprint("ai", __name__)

@ai_bp.route("/ask", methods=["POST"])
def ask():
    api_key = request.headers.get("X-API-KEY")
    if api_key != os.getenv("AGENT_API_KEY"):
        return jsonify({"error": "Unauthorized"}), 401

    question = request.json.get("question")
    return jsonify({
        "answer": f"Lio-AI a bien reçu ta question : {question}"
    })
EOF

# ---------------- PLUGIN EXEMPLE ----------------
cat <<EOF > plugins/plugin_math.py
def run(query):
    numbers = [int(x) for x in query.split() if x.isdigit()]
    return sum(numbers) if numbers else None
EOF

# ---------------- TESTS ----------------
cat <<EOF > tests/test_status.py
from flask import Flask
from routes.status import status_bp

def test_status():
    app = Flask(__name__)
    app.register_blueprint(status_bp)
    client = app.test_client()
    r = client.get("/status")
    assert r.status_code == 200
EOF

cat <<EOF > tests/test_ai.py
from flask import Flask
from routes.ai_agent import ai_bp

def test_unauthorized():
    app = Flask(__name__)
    app.register_blueprint(ai_bp)
    client = app.test_client()
    r = client.post("/ask", json={"question":"test"})
    assert r.status_code == 401
EOF

# ---------------- DOCKER ----------------
cat <<EOF > Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
EOF

# ---------------- GIT ----------------
git init
git add .
git commit -m "Initial commit Lio-AI (agent IA stable)"

echo "✅ Lio-AI créé avec succès"
echo "➡️ Prochaine étape : chmod +x setup_lio_ai_complete.sh"
