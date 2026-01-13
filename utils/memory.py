import sqlite3, numpy as np
from rag.embedder import embed_texts
DB_PATH = "data/memory.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS memory (id INTEGER PRIMARY KEY AUTOINCREMENT, user_text TEXT, response_text TEXT, embedding BLOB)")
    conn.commit()
    conn.close()

def add_memory(user_text, response_text):
    embedding = embed_texts([user_text])[0].tobytes()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO memory (user_text, response_text, embedding) VALUES (?, ?, ?)", (user_text, response_text, embedding))
    conn.commit()
    conn.close()

def search_memory(query, top_k=3):
    query_emb = embed_texts([query])[0]
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT user_text, response_text, embedding FROM memory")
    results = []
    for u,r,emb_bytes in c.fetchall():
        emb = np.frombuffer(emb_bytes, dtype=np.float32)
        score = np.dot(query_emb, emb) / (np.linalg.norm(query_emb) * np.linalg.norm(emb))
        results.append((score,u,r))
    conn.close()
    results.sort(reverse=True,key=lambda x:x[0])
    return results[:top_k]
