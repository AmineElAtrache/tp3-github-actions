import pytest

from app.web import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_message_ordinaire_est_autorise(client):
    reponse = client.post("/moderate", json={"message": "bonjour"})
    assert reponse.status_code == 200
    assert reponse.get_json() == {"decision": "autoriser"}


def test_message_contenant_le_mot_spam_est_bloque(client):
    reponse = client.post("/moderate", json={"message": "ceci est du SPAM"})
    assert reponse.status_code == 200
    assert reponse.get_json() == {"decision": "bloquer"}


@pytest.mark.parametrize(
    "corps",
    [{}, {"message": 42}],
    ids=["objet-vide", "message-non-texte"],
)
def test_message_invalide_retourne_400(client, corps):
    reponse = client.post("/moderate", json=corps)
    assert reponse.status_code == 400
    assert reponse.get_json() == {"error": "Invalid message"}


def test_message_compose_uniquement_d_espaces_est_invalide(client):
    reponse = client.post("/moderate", json={"message": "   "})
    assert reponse.status_code == 400
    assert reponse.get_json() == {"error": "Invalid message"}


def test_corps_json_de_type_liste_est_refuse(client):
    reponse = client.post("/moderate", json=["spam"])
    assert reponse.status_code == 400
    assert reponse.get_json() == {"error": "JSON object required"}
