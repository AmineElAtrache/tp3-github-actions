import pytest
from unittest.mock import patch

from app.notifications import envoyer_notification
from app.surveillance import surveiller


def test_taux_au_dessus_du_seuil_declenche_une_alerte():
    with patch("app.surveillance.envoyer_notification") as notifier:
        resultat = surveiller(0.15)
    assert resultat == "alerte"
    notifier.assert_called_once_with("Taux eleve")


def test_taux_sous_le_seuil_reste_ok_sans_notification():
    with patch("app.surveillance.envoyer_notification") as notifier:
        resultat = surveiller(0.05)
    assert resultat == "ok"
    notifier.assert_not_called()


def test_taux_exactement_egal_au_seuil_n_envoie_aucune_notification():
    with patch("app.surveillance.envoyer_notification") as notifier:
        resultat = surveiller(0.10)
    assert resultat == "ok"
    notifier.assert_not_called()


def test_panne_du_service_de_notification_est_propagee():
    with patch("app.surveillance.envoyer_notification") as notifier:
        notifier.side_effect = RuntimeError("Service non configure")
        with pytest.raises(RuntimeError, match="Service non configure"):
            surveiller(0.15)


def test_notification_reelle_signale_que_le_service_n_est_pas_configure():
    with pytest.raises(RuntimeError, match="Service non configure"):
        envoyer_notification("Taux eleve")
