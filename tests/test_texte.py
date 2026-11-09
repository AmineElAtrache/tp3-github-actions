import pytest

from app.texte import nettoyer_texte


@pytest.mark.parametrize(
    "entree, attendu",
    [
        pytest.param("  BONJOUR   monde  ", "bonjour monde", id="espaces-et-casse"),
        pytest.param(" déjà propre ", "déjà propre", id="deja-propre"),
        pytest.param("", "", id="chaine-vide"),
        pytest.param("   ", "", id="espaces-seulement"),
        pytest.param("PYTHON", "python", id="un-mot-majuscules"),
    ],
)
def test_nettoyer_texte(entree, attendu):
    assert nettoyer_texte(entree) == attendu


@pytest.mark.parametrize("entree", [123, None])
def test_nettoyer_texte_rejette_une_entree_non_textuelle(entree):
    with pytest.raises(TypeError, match="Texte attendu"):
        nettoyer_texte(entree)


def test_nettoyer_un_texte_deja_nettoye_ne_change_plus_le_resultat():
    texte = "bonjour monde"
    premiere_passe = nettoyer_texte(texte)
    seconde_passe = nettoyer_texte(premiere_passe)
    assert premiere_passe == texte
    assert seconde_passe == premiere_passe
