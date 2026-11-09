class Stock:
    def __init__(self, quantite):
        self.quantite = quantite

    def retirer(self, quantite):
        if quantite <= 0:
            raise ValueError("Quantité positive requise")
        if quantite > self.quantite:
            return False
        self.quantite -= quantite
        return True


class Reservation:
    def __init__(self, stock):
        self.stock = stock

    def reserver(self, quantite):
        if self.stock.retirer(quantite):
            return "confirmee"
        return "refusee"
