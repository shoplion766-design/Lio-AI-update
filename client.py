import requests

url = "http://localhost:5000/chat"

def ask_lio(message: str):
    response = requests.post(
        url,
        json={"message": message}  # clé 'message' correspond à ta route /chat
    )
    data = response.json()
    if "response" in data:
        return data["response"]
    else:
        return f"Erreur : {data.get('error', 'Pas de réponse')}"

if __name__ == "__main__":
    while True:
        msg = input("Vous : ")
        if msg.lower() in ["exit", "quit"]:
            break
        reply = ask_lio(msg)
        print(f"Lio : {reply}")
