# test_gpt.py
import os
from dotenv import load_dotenv
import openai
import tiktoken

# -------------------------
# Charger la clé depuis .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# -------------------------
# Test GPT-3.5
try:
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Tu es un assistant Python."},
            {"role": "user", "content": "Bonjour Lio-AI, peux-tu me saluer ?"}
        ],
        max_tokens=50
    )
    print("GPT-3.5 dit :", response.choices[0].message.content)
except Exception as e:
    print("Erreur GPT-3.5 :", e)

# -------------------------
# Test tiktoken
try:
    enc = tiktoken.get_encoding("cl100k_base")
    texte = "Bonjour Lio-AI"
    tokens = enc.encode(texte)
    print(f"Texte : {texte}")
    print(f"Tokens : {tokens}")
    print(f"Nombre de tokens : {len(tokens)}")
except Exception as e:
    print("Erreur tiktoken :", e)
