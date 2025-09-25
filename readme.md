# Exportation de bibliographie

## Champs à conserver

### Mandat initial
- Image
- Titre
- Auteur
- Éditeur
- Description
- Résumé
- Cote (pas ISBN)

## Format d'entrée

- HTML (téléchargé depuis le catalogue en ligne)

## Format de sortie

- Idéalement Word / PDF
- Le but est de l'imprimer pour afficher dans la bibliothèque

## Utilisation

- `python3 -m pip install -r requirements.txt` (à faire qu'une seule fois)
- `python3 script.py <fichier.html>`

### Pour générer un exécutable standalone

La génération de l'exécutable requiert Python 3 et les dépendances, mais l'utilisation de l'exécutable ne dépendera pas de la présence de Python sur l'ordinateur.

- `pyinstaller --onefile --add-binary "<path/to/pandoc>:pypandoc/files/" script.py`

(exemple de <path/to/pandoc> dans un venv : `venv/lib/python3.13/site-packages/pypandoc/files/pandoc`)
