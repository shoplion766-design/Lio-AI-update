import openai, os
from config import OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY
def generate_plugin(plugin_name, description):
    plugin_file = f"plugins/{plugin_name}.py"
    prompt=f"Crée un plugin Python nommé {plugin_name}.py avec description: {description}. Fonction run(query) qui retourne la réponse."
    response=openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role":"user","content":prompt}], max_tokens=400)
    code=response.choices[0].message.content.strip()
    with open(plugin_file,"w",encoding="utf-8") as f: f.write(code)
    return plugin_file
