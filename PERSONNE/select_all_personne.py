# select_all_genres.py
# OM 2020.03.26 le but est d'afficher tous les lignes de la table "t_genres" en MySql.

# Importer le fichier "select_table.py" dans lequel il y a quelques classes et méthodes en rapport avec l'affichage des données dans UNE SEULE table.
import json

from DATABASE.SELECT import select_table

try:
    # OM 2020.03.26 Une instance "select_record" pour permettre l'utilisation des méthodes de la classe DbSelectOneTable
    select_record = select_table.DbSelectOneTable()
    # Pour l'affichage du contenu suite à une requête SELECT avec un tri sur la colonne id_genre
    mysql_select_string = "SELECT * FROM T_Personne ORDER BY id_personne ASC"
    # Les résultats de la requête se trouvent dans la variable "records_select" de type <class 'list'>
    records_select = select_record.select_rows(mysql_select_string)

    # Affiche différentes formes de "sortie" des données. Il y en a beaucoup d'autres, suivant l'utilisation finale (client WEB par ex.)
    print("Type de type records_select : ",type(records_select),"Tous les résultats ", records_select, "Type des résultats ")

    for row in records_select:
        print(row['id_personne'],row['nom_pers'],row['prenom_pers'],row['date_de_naissance'],row['possession_arme'])

    for row in records_select:
        output = "id: {id_personne}  nom: {nom_pers}  prenom: {prenom_pers}  date de naissance: {date_de_naissance}  possession arme: {possession_arme}"
        print(output.format(**row))

    # Le meilleur pour la fin : le module pymysql intègre la conversion en JSON  avec "cursorclass=pymysql.cursors.DictCursor"
    # Pour vous prouver ceci, il faut importer le module JSON et vous comparer le résultat des print ci-dessous
    # Il faut absolument approcher le format JSON
    # https://developer.mozilla.org/fr/docs/Learn/JavaScript/Objects/JSON
    print("Tous les résultats déjà en JSON ", records_select)
    print(json.dumps(records_select))
    print(json.dumps(records_select, sort_keys=True, indent=4, separators=(',', ': '), default=str))

except Exception as erreur:
    # OM 2020.03.01 Message en cas d'échec du bon déroulement des commandes ci-dessus.
    print("error message: {0}".format(erreur))
