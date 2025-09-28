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

### Mise à jour 2025.09.24
On désire garder seulement :
- Image
- Titre (sans l'auteur dans le titre)
- Auteur
- Résumé
- Cote (pas ISBN)

## Format d'entrée

- HTML (téléchargé depuis le catalogue en ligne)

## Format de sortie

- Idéalement Word / PDF
- Le but est de l'imprimer pour afficher dans la bibliothèque

## Utilisation

Commencer par cloner le repo. Les commandes ci-dessous doivent être roulées depuis le root du repo.

L'utilisation d'un environnement virtuel de Python ("venv") est recommandé pour gérer les dépendances de ce projet séparément des packages installés globalement.
Pour les commandes ci-dessous, `python3` est utilisé à titre d'exemple - `python` peut être utilisé s'il pointe vers Python 3 dans l'environnement virtuel.

- `python3 -m venv venv`
- `source venv/bin/activate` (ou l'équivalent sur votre système)
- `python3 -m pip install -r requirements.txt` (à faire qu'une seule fois)
- `python3 script.py <fichier.html>`

### Pour générer un exécutable standalone

La génération de l'exécutable requiert Python 3 et les dépendances, mais l'utilisation de l'exécutable ne dépendera pas de la présence de Python sur l'ordinateur.

Ne pas oublier de remplacer `<path/to/pandoc>` dans la commande ci-dessous par l'emplacement de votre exécutable `pandoc`.
(Exemple de `<path/to/pandoc>` dans un venv sur Windows : `venv/Lib/site-packages/pypandoc/files/pandoc.exe`)

Les guillemets autour de `<path/to/pandoc>:pypandoc/files/` sont requis dans la commande.

- `pyinstaller --onefile --add-binary "<path/to/pandoc>:pypandoc/files/" script.py`

