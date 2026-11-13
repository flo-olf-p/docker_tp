# Verification du projet

Pour chaque cas, coller la commande, sa sortie, et votre explication.

1. Jeu initial de quatre articles.

Commandes : 
            - docker build -t analyse-stock:v1 . 
            Explication : cette commande construit l'image analyse-stock avec le tag v1.
            - docker run --rm -v "${PWD}/entrees:/entrees:ro" -v "${PWD}/resultats:/resultats" analyse-stock:v1 
            résultat : 
                        References : 4
                        Unites : 16
                        Valeur totale : 670.00 EUR
                        References en stock faible : 2
                        References en rupture : 1
            Explication : cette commande crée un montage volume de l'image analyse-stock:v1 avec comme entrée le dossier pour lire le fichier en "read only", et renvoie le résultat dans un fichier txt dans le dossier résultats.

2. CSV modifie sans reconstruction.

Jeu de donnée :
                article,quantite,prix_unitaire
                Clavier,10,25.00
                Souris,4,15.00
                Ecran,2,180.00
                Cable,0,8.00
                Souris,2,12.00

Réusltat : 
                References : 4
                Unites : 16
                Valeur totale : 670.00 EUR
                References en stock faible : 2
                References en rupture : 1

Explication : Après l'ajout de l'article souris avec comme quantité 2 pour un prix de 12.00€, si on relance la commande "docker run --rm -v "${PWD}/entrees:/entrees:ro" -v "${PWD}/resultats:/resultats" analyse-stock:v1", le résultat ne va pas se mettre à jour car il faut construire une nouvelle image à jour avec "docker build -t analyse-stock:v2 .".  

3. Tentative d'ecriture dans entrees en lecture seule.

Commandes : 
            - docker run --rm -v "${PWD}/entrees:/entrees:ro" analyse-stock:v1 sh -c "touch /entrees/test.txt"
            résultat : touch: cannot touch '/entrees/test.txt': Read-only file system
            Explication : Comme le fichier qu'on récupere est en lecture seul alors on ne peux pas créer, ni modifié un fichier.

4. Rapport relu depuis un autre conteneur avec le meme volume nomme.

Commandes : 
            - docker volume create volume-resultats
            - docker run --rm -v "${PWD}/entrees:/entrees:ro" -v "volume-resultats:/resultats" analyse-stock:v1
            - docker run --rm -v "volume-resultats:/resultats:ro" ubuntu:24.04 cat /resultats/bilan-stock.txt
            résultat : 
                        References : 4
                        Unites : 16
                        Valeur totale : 670.00 EUR
                        References en stock faible : 2
                        References en rupture : 1
            Explication : Ici on crée un volume volume-resultats, puis on lance l'image analyse-stock:v1 et après on relit le bilan-stock.txt en regardant s'il y a ubuntu:24.04.

5. Entree absente, vide ou invalide.

Commandes : 
            - docker run --rm analyse-stock:v1
            résultat : Erreur : [Errno 2] No such file or directory: '/entrees/stock.csv'
            Explication : Étant donné qu'il manque l'entrée, le Python ne peut pas se lancer car il ne peut pas ouvrir le stock.csv.

