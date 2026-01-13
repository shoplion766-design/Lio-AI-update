from flask import Flask
from routes.status import status_bp
from routes.example_api import example_bp
from routes.ai_agent import ai_bp

app = Flask(__name__)
app.register_blueprint(status_bp)
app.register_blueprint(example_bp)
app.register_blueprint(ai_bp)

@app.route("/")
def home(): return "Hello, Lio-AI Copilot GPT-3.5 is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
