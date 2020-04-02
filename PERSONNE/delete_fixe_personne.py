# delete_fixe_genres.py
# OM 2020.03.10 le but est d'effacer une ligne d'une table en MySql.
# On doit modifier la valeur de la variable "numero_ligne_table_delete"
# Si on démarre ce fichier plusieurs fois, alors MySql ne renvoie pas d'erreur, car effacer une ligne inexistante dans une table
# ce n'est pas considéré comme une erreur, mais simplement MySql renvoie le nombre de lignes effacées dans ce cas : 0 lignes effacées.

# Importer le fichier "delete_fixe_one_rec_one_table.py" dans lequel il y a quelques classes et méthodes en rapport avec la suppression des données dans UNE SEULE table.
from DATABASE.DELETE import delete_one_record_one_table

try:
    # OM 2020.01.28 Une instance "delete_record" pour permettre l'utilisation des méthodes de la classe DbDeleteOneTable
    delete_record = delete_one_record_one_table.DbDeleteOneTable()
    # OM 2020.01.28 Impose le numéro de la ligne à effacer dans la table.
    # A changer à la main pour essayer sur votre BD.
    numero_ligne_table_delete = 3
    # OM 2020.03.11 Fonction DELETE avec le numéro de la ligne à effacer passée en paramètre.
    delete_record.delete_one_record_one_table("""DELETE FROM T_Personne WHERE id_personne = %(no_ligne_delete)s""",numero_ligne_table_delete)

except Exception as erreur:
    # OM 2020.03.01 Message en cas d'échec du bon déroulement des commandes ci-dessus.
    print("error message: {0}".format(erreur))
