import os, openai
from config import OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY
def propose_refactor(file_path):
    if not os.path.exists(file_path):
        return None
    with open(file_path,"r",encoding="utf-8") as f: code=f.read()
    prompt=f"Refactore ce code Python pour optimisation:\n{code}\nRetourne uniquement le code."
    response=openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role":"user","content":prompt}], max_tokens=1200)
    return response.choices[0].message.content.strip()
