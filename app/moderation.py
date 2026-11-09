def decider(modele, message):
    classe = modele.predict(message)
    if classe == "spam":
        return "bloquer"
    return "autoriser"
