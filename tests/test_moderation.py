import pytest
from unittest.mock import Mock

from app.moderation import decider


def test_classe_spam_donne_la_decision_bloquer():
    # Arrange
    modele = Mock()
    modele.predict.return_value = "spam"
    # Act
    decision = decider(modele, "Offre miracle")
    # Assert
    assert decision == "bloquer"
    modele.predict.assert_called_once_with("Offre miracle")


def test_classe_normal_donne_la_decision_autoriser():
    # Arrange
    modele = Mock()
    modele.predict.return_value = "normal"
    # Act
    decision = decider(modele, "Bonjour à tous")
    # Assert
    assert decision == "autoriser"
    modele.predict.assert_called_once_with("Bonjour à tous")


def test_decider_propage_l_erreur_si_le_modele_est_indisponible():
    # Arrange
    modele = Mock()
    modele.predict.side_effect = RuntimeError("Modele indisponible")
    # Act / Assert
    with pytest.raises(RuntimeError, match="Modele indisponible"):
        decider(modele, "Offre miracle")
