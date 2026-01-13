def run(query):
    if "addition" in query or "somme" in query:
        parts = [int(s) for s in query.split() if s.isdigit()]
        return f"Résultat de l’addition: {sum(parts)}"
    return None
