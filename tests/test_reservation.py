import pytest

from app.reservation import Reservation, Stock


@pytest.fixture
def stock():
    return Stock(5)


def test_reservation_de_2_unites_est_confirmee_et_diminue_le_stock(stock):
    # Arrange
    reservation = Reservation(stock)
    # Act
    statut = reservation.reserver(2)
    # Assert
    assert statut == "confirmee"
    assert stock.quantite == 3


def test_reservation_de_6_unites_est_refusee_sans_changer_le_stock(stock):
    # Arrange
    reservation = Reservation(stock)
    # Act
    statut = reservation.reserver(6)
    # Assert
    assert statut == "refusee"
    assert stock.quantite == 5


def test_reservation_de_5_unites_epuise_le_stock(stock):
    # Arrange
    reservation = Reservation(stock)
    # Act
    statut = reservation.reserver(5)
    # Assert
    assert statut == "confirmee"
    assert stock.quantite == 0


def test_reservation_quantite_nulle_leve_valueerror_et_laisse_le_stock_intact(stock):
    # Arrange
    reservation = Reservation(stock)
    # Act / Assert
    with pytest.raises(ValueError, match="Quantité positive requise"):
        reservation.reserver(0)
    assert stock.quantite == 5
