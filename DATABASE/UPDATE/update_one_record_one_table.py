# update_one_record_one_table.py
# OM 2020.03.26 le but est de mettre à jour un champ dans une ligne pour une seule table.
import pymysql

from DATABASE import connect_db


class DbUpdateOneTable():

    # Constructeur, à chaque instanciation de cette classe "DbUpdateOneTable()" les lignes de code de la méthode "__init__ (self)" sont interprétées.
    def __init__(self):
        print("Constructeur CLASSE DbUpdateOneTable")

    def update_one_record_one_table(self, requete_update_mysql, valeurs_update):
        """
        Méthode qui permet de mettre à jour une ligne d'une table.
        OM 2020.03.26
                Parametres:
                        requete_update_mysql (class 'str'): la requête UPDATE MySql
                        valeurs_update (class 'int'): valeurs pour la mise à jour
                Retourne:
                        pas de valeurs
        """
        try:
            # OM 2020.01.28 CONNECTION A LA BD
            self.connection_dbc = connect_db.DatabaseTools()
            # Un simple test qui renvoie un message dans la console suivant l'état de la BD
            self.connection_dbc.is_connection_open()

            # Pour aider à comprendre les types de données on affiche dans la console.
            print("type >>> requete_update_mysql ",type(requete_update_mysql), requete_update_mysql )
            print("type >>> valeurs_update ",type(valeurs_update), valeurs_update)
            # Afficher les docstrings...très importantes pour votre projet.
            print(self.update_one_record_one_table.__doc__)

            # OM 2020.03.11 Execute la requête avec un passage de paramètres
            self.connection_dbc.DBcursor.execute(requete_update_mysql, valeurs_update)
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