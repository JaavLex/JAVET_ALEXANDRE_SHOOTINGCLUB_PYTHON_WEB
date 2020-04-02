# insert_genres_one_value.py
# OM 2698.03.21 Démonstration de l'insertion d'une valeur dans un champ d'une table.

from DATABASE import connect_db
# Importer le fichier "InsertOneTable" dans lequel il y a quelques classes et méthodes en rapport avec le sujet d'insertion dans UNE SEULE table.
from DATABASE.INSERT import insert_one_table

try:
    # OM 2020.01.28 Une instance "insert_records" pour permettre l'utilisation des méthodes de la classe DbInsertOneTable
    insert_records = insert_one_table.DbInsertOneTable()

    nom = "Maccro"
    prenom = "Oliver"
    dob = "1889-01-20"
    possarm = 1
    # Ligne pour afficher la valeur dans la console...c'est tout
    print("value_nom", nom, "value_prenom", prenom, "value_date_naissance", dob, "value_possession", possarm)


    valeurs_insertion_dictionnaire2 = {'value_nom': nom, 'value_prenom': prenom, 'value_date_naissance': dob, 'value_possession': possarm}

    # OM 2020.01.28 Pour éviter les injections SQL, il est possible de passer les valeurs à insérer sous forme "paramètrée" (avec le %(...)s au lieu de %s)
    # Pour les vrais geeks et geeketes consulter le site ci-dessous.
    # L'insertion de données est vraiment TROP inspirée du site suivant MERCI !!! https://realpython.com/prevent-python-sql-injection/
    # Dans la requête SQL le mot clé IGNORE est là pour TRANSFORMER une erreur SQL en une WARNING
    mysql_insert_string = "INSERT IGNORE INTO T_Personne (id_personne, nom_pers, prenom_pers, date_de_naissance, possession_arme) VALUES (null, %(value_nom)s, %(value_prenom)s, %(value_date_naissance)s, %(value_possession)s )"

    # Insertion de la valeur définie dans la variable "valeur_debile_mais_presque_aleatoire_a_inserer"
    # dans la table "t_genres"
    insert_records.insert_one_record_many_values_one_table(mysql_insert_string,
                                               valeurs_insertion_dictionnaire2)

except Exception as erreur:
    # OM 2020.03.01 Message en cas d'échec du bon déroulement des commandes ci-dessus.
    print("Message erreur {0}".format(erreur))