import pytest

from app.livraison import frais_livraison


def test_livraison_panier_ordinaire():
    # Arrange
    montant = 120
    # Act
    resultat = frais_livraison(montant)
    # Assert
    assert resultat == 25


def test_livraison_juste_sous_le_seuil():
    # Arrange
    montant = 299
    # Act
    resultat = frais_livraison(montant)
    # Assert
    assert resultat == 25


def test_livraison_gratuite_au_seuil_inclus():
    # Arrange — la règle indique « à partir de 300 DH inclus »
    montant = 300
    # Act
    resultat = frais_livraison(montant)
    # Assert
    assert resultat == 0


def test_livraison_gratuite_au_dessus_du_seuil():
    # Arrange
    montant = 301
    # Act
    resultat = frais_livraison(montant)
    # Assert
    assert resultat == 0


def test_livraison_panier_a_zero():
    # Arrange
    montant = 0
    # Act
    resultat = frais_livraison(montant)
    # Assert
    assert resultat == 25


def test_livraison_montant_negatif_leve_valueerror():
    # Arrange
    montant = -1
    # Act / Assert
    with pytest.raises(ValueError, match="Montant negatif"):
        frais_livraison(montant)
