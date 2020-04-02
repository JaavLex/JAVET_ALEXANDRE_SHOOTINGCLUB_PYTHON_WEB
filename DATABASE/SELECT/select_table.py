# select_table.py
# OM 2020.03.10 le but est d'afficher toutes les colonnes d'une seule table.
import pymysql

from DATABASE import connect_db

class DbSelectOneTable():

    # Constructeur, à chaque instanciation de cette classe "DbSelectOneTable()" les lignes de code de la méthode "__init__ (self)" sont interprétées.
    def __init__(self):
        print("Constructeur CLASSE DbSelectOneTable")

    def select_rows(self, requete_select_mysql):
        """
        Méthode qui permet d'afficher le contenu de la BD selon la requête SELECT.
        OM 2020.03.26
                Parametres:
                        requete_select_mysql (class 'str'): la requête SELECT MySql
                Retourne:
                        pas de valeurs
        """
        try:
            # OM 2020.01.28 CONNECTION A LA BD
            self.connection_dbc = connect_db.DatabaseTools()
            # Un simple test qui renvoie un message dans la console suivant l'état de la BD
            self.connection_dbc.is_connection_open()

            # OM 2020.03.11 Execute la requête
            self.connection_dbc.DBcursor.execute(requete_select_mysql)
            # Retourne les résultats de la requête
            data_select = self.connection_dbc.DBcursor.fetchall()
            return data_select
            self.connection_dbc.DBcursor.close()

        except Exception as erreur:
            # OM 2020.03.01 Message en cas d'échec du bon déroulement des commandes ci-dessus.
            print("error message: {0}".format(erreur))
        finally:
            # On ferme le curseur et la base de donnée et on affiche un message dans la console.
            self.connection_dbc.DBcursor.close()
            self.connection_dbc.close_connection()
            print("DBcursor et DB fermés")