# update_fixe_genre.py
# OM 2020.03.26 le but est de mettre à jour une ligne d'une table en MySql.
# On doit modifier la valeur de la variable "numero_ligne_table_update"
# On doit modifier le contenu de la "valeur_genre"

# Importer le fichier "update_one_record_one_table.py" dans lequel il y a quelques classes et méthodes en rapport avec la mise à jour des données dans UNE SEULE table.
from DATABASE.UPDATE import update_one_record_one_table

try:
    # OM 2020.03.26 Une instance "update_record" pour permettre l'utilisation des méthodes de la classe DbUpdateOneTable
    update_record = update_one_record_one_table.DbUpdateOneTable()

    # OM 2020.03.26 Impose le numéro de la ligne à mettre à jour dans la table t_genres.
    # A changer à la main pour essayer sur votre BD.
    numero_ligne_table_update = 5

    # Définir une valeur pour la mise à jour du champ "intitule_genre"
    nom = "clowneriea"
    # Afficher la valeur dans la console...c'est tout, vraiment tout !
    print("valeur_nom ",nom, "; numero_ligne_table_update ",numero_ligne_table_update)

    # OM 2020.03.26 Pour éviter les injections SQL, il est possible de passer les valeurs à mettre à jour sous forme "paramètrée" (avec le %(...)s au lieu de %s)
    # Pour les vrais geeks et geeketes consulter le site ci-dessous.
    # La mise à jour de données est vraiment TROP inspirée du site suivant MERCI !!! https://realpython.com/prevent-python-sql-injection/

    # On défint un dictionnaire pour passer les 2 valeurs en paramètre de façon un "peu" sécurisée dans la BD
    # on voit ainsi la corresp ondance des positions entre les attributs et les valeurs définies en python
    valeur_update_dictionnaire = {'value_nom': nom, 'no_ligne_update': numero_ligne_table_update}

    # Pour la mise à jour on doit avoir au moins deux valeurs "numero_ligne_table_update" et "valeur_genre"
    mysql_update_string = "UPDATE T_Personne SET nom_pers = %(value_nom)s WHERE id_personne = %(no_ligne_update)s"

    # OM 2020.03.26 Fonction UPDATE avec le numéro de la ligne à mettre à jour et la nouvelle valeur du champ "intitule_genre"
    update_record.update_one_record_one_table(mysql_update_string,
                                              valeur_update_dictionnaire)

except Exception as erreur:
    # OM 2020.03.01 Message en cas d'échec du bon déroulement des commandes ci-dessus.
    print("error message: {0}".format(erreur))
