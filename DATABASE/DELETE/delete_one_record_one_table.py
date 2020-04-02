# delete_fixe_one_rec_one_table.py
# OM 2020.03.10 le but est d'effacer une ligne d'une table en MySql.

import pymysql
import warnings

from DATABASE import connect_db

# OM 2020.03.02 Mécanisme ingénieux qui filtre les warnings et les associes
# pour être traitées comme des erreurs dans le code Python.
# détecte la suite de caractères "Duplicate entry." dans un message de warnings
# et convertit le warnings en action "error"
warnings.filterwarnings(
  action="error",
  message=".*Duplicate entry.*",
  category=pymysql.Warning
)

# détecte la suite de caractères "1265." dans un message de warnings
# et convertit le warnings en action "error"
warnings.filterwarnings(
  action="error",
  message=".*1265.*",
  category=pymysql.Warning
)

class DbDeleteOneTable():

    # Constructeur, à chaque instanciation de cette classe "DbInsertOneTable()" les lignes de code de la méthode "__init__ (self)" sont interprétées.
    def __init__ (self):
        print("Constructeur CLASSE DbDeleteOneTable")

    def delete_one_record_one_table(self, requete_delete_mysql, num_ligne_delete):
        """
        Méthode qui permet d'effacer une ligne d'une table.
        OM 2020.03.24
                Parametres:
                        requete_delete_mysql (class 'str'): la requête DELETE MySql
                        num_ligne_delete (class 'int'): numéro de la ligne à effacer
                Retourne:
                        pas de valeurs
        """
        try:
            # OM 2020.01.28 CONNECTION A LA BD
            self.connection_dbc = connect_db.DatabaseTools()
            # Un simple test qui renvoie un message dans la console suivant l'état de la BD
            self.connection_dbc.is_connection_open()

            # Pour aider à comprendre les types de données on affiche dans la console.
            print("type >>> requete_delete_mysql ",type(requete_delete_mysql))
            print("type >>> num_ligne_delete ",type(num_ligne_delete))
            # Afficher les docstrings...très importantes pour votre projet.
            print(self.delete_one_record_one_table.__doc__)

            # OM 2020.03.11 Execute la requête avec un passage de paramètres
            self.connection_dbc.DBcursor.execute(requete_delete_mysql, {'no_ligne_delete' : num_ligne_delete})
            # OM 2020.03.11 L'instruction suivante est indispensable pour confirmer l'effacement des données (en cas de problèmes : rollback)
            self.connection_dbc.db.commit()
            self.connection_dbc.DBcursor.close()
        except pymysql.Error as error:
            # OM 2020.03.11 L'instruction suivante est indispensable pour confirmer l'effacement des données (en cas de problèmes : rollback)
            self.connection_dbc.db.rollback()
            print(" Il y a une ERREUR : %s", error)
            print("connection_dbc.db.rollback() insertOneRecord")
        except pymysql.DataError as error1:
            # OM 2020.03.11 L'instruction suivante est indispensable pour confirmer l'effacement des données (en cas de problèmes : rollback)
            self.connection_dbc.db.rollback()
            print(" Il y a une DataError : %s", error1)
            print("connection_dbc.db.rollback() insertOneRecord")
        except pymysql.DatabaseError as error2:
            # OM 2020.03.11 L'instruction suivante est indispensable pour confirmer l'effacement des données (en cas de problèmes : rollback)
            self.connection_dbc.db.rollback()
            print(" Il y a une DatabaseError : %s", error2)
            print("connection_dbc.db.rollback() insertOneRecord")
        except pymysql.Warning as error3:
            # OM 2020.03.11 L'instruction suivante est indispensable pour confirmer l'effacement des données (en cas de problèmes : rollback)
            self.connection_dbc.db.rollback()
            print(" Il y a une Warning : %s", error3)
            print("connection_dbc.db.rollback() insertOneRecord")
        except pymysql.MySQLError as error4:
            # OM 2020.03.11 L'instruction suivante est indispensable pour confirmer l'effacement des données (en cas de problèmes : rollback)
            self.connection_dbc.db.rollback()
            print(" Il y a une MySQLError : %s", error4)
            print("connection_dbc.db.rollback() insertOneRecord")
        except pymysql.IntegrityError as error5:
            # OM 2020.03.11 L'instruction suivante est indispensable pour confirmer l'effacement des données (en cas de problèmes : rollback)
            self.connection_dbc.db.rollback()
            print(" Il y a une IntegrityError : %s", error5)
            print("connection_dbc.db.rollback() insertOneRecord")
        except:
            # OM 2020.03.11 L'instruction suivante est indispensable pour confirmer l'effacement des données (en cas de problèmes : rollback)
            self.connection_dbc.db.rollback()
            print("Unknown error occurred")
        finally:
            # On ferme le curseur et la base de donnée et on affiche un message dans la console.
            self.connection_dbc.DBcursor.close()
            self.connection_dbc.close_connection()
            print("DBcursor et DB fermés")