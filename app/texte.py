def nettoyer_texte(texte):
    if not isinstance(texte, str):
        raise TypeError("Texte attendu")
    return " ".join(texte.lower().split())
