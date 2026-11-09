from app.notifications import envoyer_notification


def surveiller(taux_erreur):
    if taux_erreur > 0.10:
        envoyer_notification("Taux eleve")
        return "alerte"
    return "ok"
