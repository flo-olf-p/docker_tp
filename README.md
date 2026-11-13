# Analyse de stock avec Docker

## Auteurs
Florian Pleigneur
Tristan Fabre

## Construction
La commande de construction est : docker build -t analyse-stock:v1 .

Notre Dockerfile se compose des commandes suivantes :
- FROM ubuntu:24.04 signifie que l'on part de l'image ubuntu 24.04

- RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 \
    && rm -rf /var/lib/apt/lists/* indique que l'on souhaite installer python pendant la construction de l'image

- WORKDIR /app crée et choisit le dossier app comme dossier de travail

- COPY stock.py . copie le programme dans le dossier app 

- CMD ["python3", "stock.py"] exécute ce programme par défaut au lancement du conteneur

## Execution avec montages
Commande :
- docker run --rm -v "${PWD}/entrees:/entrees:ro" -v "${PWD}/resultats:/resultats" analyse-stock:v1

Cette commande crée et exécute le conteneur en montant l'entrée et la sortie, ce qui fait que les informations sont stockées directement sur l'ordinateur.
Le chemin en entrée va chercher dans le dossier entrees le fichier stock.csv depuis le programme python, puis écrit le résultat dans un dossier resultats sous la forme d'un document texte nommé bilan-stock.txt

## Tests et resultats
Pour tester et visualiser les résultats du projet, dirigez vous vers le fichier preuves/verification.md

## Reproduction après git clone
Après avoir cloné le projet, suivez ces étapes pour obtenir les résultats.

- Ouvrir le terminal dans le dossier du projet, puis exécuter cette commande en veillant à avoir Docker Engine pour construire l'image : docker build -t analyse-stock:v1 .
- Exécuter la commande suivante qui va lancer un conteneur et afficher le résultat dans le terminal : docker run --rm -v "${PWD}/entrees:/entrees:ro" -v "${PWD}/resultats:/resultats" analyse-stock:v1
De plus, elle a également créée le fichier bilan-stock.txt dans le dossier resultats généré automatiquement.