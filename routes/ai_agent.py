from flask import Blueprint, request, jsonify
import openai, os, importlib
from config import OPENAI_API_KEY, MAX_TOKENS, AGENT_API_KEY
from rag.loader import load_knowledge
from rag.embedder import embed_texts
from rag.retriever import retrieve
from utils.memory import init_db, add_memory, search_memory
from auto_refactor.plugin_generator import generate_plugin
from auto_refactor.refactor import propose_refactor

ai_bp = Blueprint("ai_agent", __name__)
openai.api_key = OPENAI_API_KEY

init_db()
knowledge = load_knowledge()
texts = knowledge["text"].tolist()
embeddings = embed_texts(texts)

PLUGINS = []
for f in os.listdir("plugins"):
    if f.endswith(".py") and f != "__init__.py":
        module = importlib.import_module("plugins." + f[:-3])
        PLUGINS.append(module)

@ai_bp.route("/ask", methods=["POST"])
def ask_ai():
    key = request.headers.get("X-API-KEY")
    if key != AGENT_API_KEY: return jsonify({"error":"Unauthorized"}),401
    data=request.get_json(); question=data.get("question","").strip()
    if not question: return jsonify({"error":"Question vide"}),400

    for plugin in PLUGINS:
        result=plugin.run(question)
        if result: add_memory(question,result); return jsonify({"answer":result,"plugin":plugin.__name__})

    context_rag = retrieve(embed_texts([question])[0], embeddings, texts)
    context_memory = [r[2] for r in search_memory(question)]
    prompt=f"Tu es Lio-AI Copilot GPT-3.5.\nCONTEXTE RAG:\n{context_rag}\nCONTEXTE MEMOIRE:\n{context_memory}\nQUESTION:\n{question}"
    try:
        response=openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role":"user","content":prompt}], max_tokens=MAX_TOKENS, timeout=20)
        answer=response.choices[0].message.content.strip()
        add_memory(question,answer)
        return jsonify({"answer":answer,"context_rag":context_rag,"context_memory":context_memory})
    except Exception as e: return jsonify({"error":str(e)}),500

@ai_bp.route("/admin/refactor", methods=["POST"])
def refactor_code():
    data=request.get_json(); file_path=data.get("file_path")
    if not file_path: return {"error":"file_path manquant"},400
    new_code=propose_refactor(file_path)
    if new_code:
        with open(file_path,"w",encoding="utf-8") as f: f.write(new_code)
        return {"success":True,"file_refactored":file_path}
    return {"success":False,"message":"Pas de modification"}

@ai_bp.route("/admin/new_plugin", methods=["POST"])
def new_plugin():
    data=request.get_json(); plugin_name=data.get("plugin_name"); description=data.get("description")
    if not plugin_name or not description: return {"error":"plugin_name ou description manquant"},400
    path=generate_plugin(plugin_name,description)
    return {"success":True,"plugin_created":path}
