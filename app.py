import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import openai
import tiktoken

# Charger les variables d'environnement depuis .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Initialiser tiktoken pour cl100k_base (GPT-3.5 / GPT-4)
encoder = tiktoken.get_encoding("cl100k_base")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json or {}
    question = data.get("question") or request.form.get("question")
    
    if not question:
        return jsonify({"error": "Aucune question fournie"}), 400

    # Compter les tokens
    tokens = encoder.encode(question)
    token_count = len(tokens)

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un assistant Python."},
                {"role": "user", "content": question}
            ],
            max_tokens=150
        )
        answer = response.choices[0].message.content

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({
        "question": question,
        "answer": answer,
        "tokens": tokens,
        "token_count": token_count
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
