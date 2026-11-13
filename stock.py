import argparse
import csv
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path


def calculer_statistiques(articles):
    # Chaque article est (nom, quantite, prix_unitaire).
    # La quantite est un int ; le prix est un Decimal.
    # TODO : calculer les cinq indicateurs demandes dans la fiche TP.
    # Renvoyer un dictionnaire avec ces cles :
    # references, unites, valeur, faibles, ruptures.
    #raise NotImplementedError("Completez calculer_statistiques.")

    dictionnaire = {}

    nb_unites = 0
    valeur_totale = 0
    references_faibles = 0
    references_ruptures = 0

    for i in range (0, len(articles), 1):
        nb_unites += articles[i][1]
        valeur_totale += articles[i][2] * articles[i][1]

         # Gestion des articles en rupture
        if(articles[i][1] == 0):
            references_ruptures += 1
        # Gestion des articles en stock bas
        if(articles[i][1] < 5 and articles[i][1] != 0):
            references_faibles += 1

           


    dictionnaire["references"] = len(articles)
    dictionnaire["unites"] = nb_unites
    dictionnaire["valeur"] = valeur_totale
    dictionnaire["faibles"] = references_faibles
    dictionnaire["ruptures"] = references_ruptures

    return dictionnaire



def lire_articles(source):
    with source.open(encoding="utf-8-sig", newline="") as fichier:
        lecteur = csv.DictReader(fichier)
        if lecteur.fieldnames != ["article", "quantite", "prix_unitaire"]:
            raise ValueError("Colonnes : article,quantite,prix_unitaire")
        articles = []
        for ligne in lecteur:
            nom = ligne["article"]
            quantite = int(ligne["quantite"])
            prix = Decimal(ligne["prix_unitaire"])
            if not nom or quantite < 0 or not prix.is_finite() or prix < 0:
                raise ValueError("Nom requis, quantite et prix non negatifs.")
            articles.append((nom, quantite, prix))
    if not articles:
        raise ValueError("Le fichier ne contient aucun article.")
    return articles


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--entree", default="/entrees/stock.csv")
    parser.add_argument("--sortie", default="/resultats/bilan-stock.txt")
    args = parser.parse_args()
    try:
        stats = calculer_statistiques(lire_articles(Path(args.entree)))
        rapport = "\n".join([
            f"References : {stats['references']}",
            f"Unites : {stats['unites']}",
            f"Valeur totale : {stats['valeur']:.2f} EUR",
            f"References en stock faible : {stats['faibles']}",
            f"References en rupture : {stats['ruptures']}",
        ]) + "\n"
        sortie = Path(args.sortie)
        sortie.parent.mkdir(parents=True, exist_ok=True)
        sortie.write_text(rapport, encoding="utf-8")
    except (OSError, ValueError, InvalidOperation, TypeError, NotImplementedError) as erreur:
        print(f"Erreur : {erreur}", file=sys.stderr)
        return 2
    print(rapport, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
