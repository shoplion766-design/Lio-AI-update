import os
import gradio as gr
from openai import OpenAI

# Vérifie que la clé API est définie
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("La variable d'environnement OPENAI_API_KEY n'est pas définie.")

# Initialise le client OpenAI
client = OpenAI(api_key=api_key)

# Fonction pour interroger OpenAI
def ask_openai(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Erreur OpenAI: {e}"

# Interface Gradio
with gr.Blocks() as demo:
    gr.Markdown("## Lio-AI Agent")
    with gr.Row():
        user_input = gr.Textbox(label="Pose ta question ici")
        submit_btn = gr.Button("Envoyer")
    output_text = gr.Textbox(label="Réponse de Lio-AI")
    
    submit_btn.click(fn=ask_openai, inputs=user_input, outputs=output_text)

# Lancement du serveur Gradio
demo.launch(server_name="0.0.0.0", server_port=7860)
