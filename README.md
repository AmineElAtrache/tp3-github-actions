# TP3 : GitHub Actions

Dépôt public : https://github.com/AmineElAtrache/tp3-github-actions

## Projet et installation

Le projet du TP2 a été repris depuis `../TP1/tp_tests` dans l'arborescence locale des TPs (ce dossier contient les rapports TP2). Les sources `app/` et les tests `tests/` sont conservés sans modification.

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -v --cov=app --cov-report=term-missing --cov-fail-under=80
```

Les dépendances sont pytest, pytest-cov et Flask, nécessaire aux tests de `app/web.py`.

## Exercice 1 : premier workflow

`.github/workflows/hello.yml` affiche un message, la version Python préinstallée, le répertoire courant (`pwd`), les fichiers (`ls -la`), la branche, le commit et l'événement GitHub.

Exécution push réussie après correction : https://github.com/AmineElAtrache/tp3-github-actions/actions/runs/42632726685

Runner observé : Ubuntu ; Python préinstallé 3.12.3 ; répertoire `/home/runner/work/tp3-github-actions/tp3-github-actions`.
Le workflow hello ne fait pas de checkout : `ls -la` affiche le contenu initial du workspace du runner. Le pipeline de tests récupère explicitement le dépôt avec checkout.

## Exercice 2 : déclencheurs et échec volontaire

Les deux déclencheurs de hello sont `push` et `workflow_dispatch`.
Dans GitHub : **Actions > Premier workflow CI > Run workflow > main > Run workflow**.
Les lancements manuels de ce TP ont été effectués avec GitHub CLI, qui utilise le même événement `workflow_dispatch` que ce bouton.

- Push initial réussi : https://github.com/AmineElAtrache/tp3-github-actions/actions/runs/42631462744
- Lancement manuel initial réussi, sur le même commit `45f0795` : https://github.com/AmineElAtrache/tp3-github-actions/actions/runs/42632319065
- Lancement manuel de la version finale : https://github.com/AmineElAtrache/tp3-github-actions/actions/runs/42632774683

Le push part automatiquement après l'envoi d'un commit ; le lancement manuel est demandé sur une branche choisie. Pour les deux lancements initiaux, le code exécuté était identique. Dans les journaux, `GITHUB_EVENT_NAME` distingue `push` et `workflow_dispatch`, `GITHUB_REF_NAME` donne la branche et `GITHUB_SHA` identifie le commit exécuté.

Échec volontaire observé : https://github.com/AmineElAtrache/tp3-github-actions/actions/runs/42632432795

L'étape **Erreur volontaire** exécutait `exit 1`. Le job `hello` a échoué avec le code 1 ; **Étape après l'erreur** a été ignorée (`skipped`). Les étapes précédentes ont réussi. L'erreur a ensuite été supprimée ; la version finale réussit.

## Exercice 3 : tests et couverture

`.github/workflows/ci.yml`, nommé **CI - Tests Python**, s'exécute à chaque push et peut aussi être lancé manuellement. Le job `tests` utilise Ubuntu, `actions/checkout@v6`, `actions/setup-python@v7` avec Python 3.12, puis installe `requirements-dev.txt`. Le cache pip utilise explicitement ce fichier.

Exécution push vérifiée : https://github.com/AmineElAtrache/tp3-github-actions/actions/runs/42632726609

Résultats observés le 9 novembre 2026 :

- Python 3.12.16 installé ; dépendances installées correctement.
- 33 tests collectés, 33 réussis, 0 échoué.
- Couverture des lignes exécutables : **100 %**, 55 instructions, 0 manquante.
- Tous les modules de `app/` sont couverts à 100 %. La colonne `Missing` est vide : aucune ligne non couverte à identifier.
- Cette mesure concerne les lignes ; elle ne démontre pas que toutes les branches ou tous les cas possibles sont testés.

### Expériences sur les seuils

Chaque seuil a été réellement exécuté sur GitHub, sur le commit `19432d4` :

| Seuil | Couverture | Résultat | Exécution |
| --- | --- | --- | --- |
| 50 % | 100 % | Réussite | [Journaux](https://github.com/AmineElAtrache/tp3-github-actions/actions/runs/42632730994) |
| 70 % | 100 % | Réussite | [Journaux](https://github.com/AmineElAtrache/tp3-github-actions/actions/runs/42632740566) |
| 80 % | 100 % | Réussite | [Journaux](https://github.com/AmineElAtrache/tp3-github-actions/actions/runs/42632748843) |
| 90 % | 100 % | Réussite | [Journaux](https://github.com/AmineElAtrache/tp3-github-actions/actions/runs/42632756132) |
| 100 % | 100 % | Réussite | [Journaux](https://github.com/AmineElAtrache/tp3-github-actions/actions/runs/42632765533) |

Aucun seuil demandé ne fait échouer ce projet : la couverture atteint déjà 100 %. Le pipeline échouerait si la couverture mesurée devenait inférieure au seuil choisi. Le seuil automatique final reste **80 %**.

Pour reproduire : **Actions > CI - Tests Python > Run workflow**, choisir le seuil puis lancer. Ou :

```bash
gh workflow run ci.yml --ref main -f coverage=100
```

Les essais intermédiaires ont révélé un chemin de cache pip à préciser ; il a été corrigé avec `cache-dependency-path: requirements-dev.txt`. Les liens ci-dessus désignent les exécutions corrigées.
