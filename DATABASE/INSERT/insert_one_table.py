# insert_one_table.py
# OM 2020.03.10 le but est d'insérer des valeurs en MySql dans une seule table
import pymysql
from DATABASE import connect_db

class DbInsertOneTable():

    # Constructeur, à chaque instanciation de cette classe "DbInsertOneTable()" les lignes de code de la méthode "__init__ (self)" sont interprétées.
    def __init__ (self):
        print("Constructeur CLASSE DbInsertOneTable")

    def insert_one_record_one_table(self, requete_insert_mysql, valeurs_a_inserer):
        """
        Méthode qui permet d'insérer UNE seule valeur passée en paramètre.
        OM 2020.03.24
                Parametres:
                        requete_insert_mysql (class 'str'): une classe string
                        valeurs_insertion (class 'dict'): une classe dictionnaire
                Retourne:
                        pas de valeurs
        """
        try:
            # OM 2020.01.28 CONNECTION A LA BD
            self.connection_dbc = connect_db.DatabaseTools()
            # Un simple test qui renvoie un message dans la console suivant l'état de la BD
            self.connection_dbc.is_connection_open()

            # Pour aider à comprendre les types de données on affiche dans la console
            print("type >>> requete_insert_mysql ",type(requete_insert_mysql))
            print("type >>> valeurs_a_inserer ",type(valeurs_a_inserer))
            # OM 2020.03.11 Execute la requête avec un passage de paramètres
            self.connection_dbc.DBcursor.execute(requete_insert_mysql, {'values_insert' : valeurs_a_inserer})

            # OM 2020.03.11 L'instruction suivante est indispensable pour confirmer l'insertion des données (en cas de problèmes : rollback)
            self.connection_dbc.db.commit()

        except pymysql.Error as error:
            # OM 2020.03.11 L'instruction suivante est indispensable pour annuler l'insertion des données (commande opposée : COMMIT)
            self.connection_dbc.db.rollback()
            print(" Il y a une ERREUR : %s", error)
            print("connection_dbc.db.rollback() insertOneRecord")
        except pymysql.DataError as error1:
            # OM 2020.03.11 L'instruction suivante est indispensable pour annuler l'insertion des données (commande opposée : COMMIT)
            self.connection_dbc.db.rollback()
            print(" Il y a une DataError : %s", error1)
            print("connection_dbc.db.rollback() insertOneRecord")
        except pymysql.DatabaseError as error2:
            # OM 2020.03.11 L'instruction suivante est indispensable pour annuler l'insertion des données (commande opposée : COMMIT)
            self.connection_dbc.db.rollback()
            print(" Il y a une DatabaseError : %s", error2)
            print("connection_dbc.db.rollback() insertOneRecord")
        except pymysql.Warning as error3:
            # OM 2020.03.11 L'instruction suivante est indispensable pour annuler l'insertion des données (commande opposée : COMMIT)
            self.connection_dbc.db.rollback()
            print(" Il y a une Warning : %s", error3)
            print("connection_dbc.db.rollback() insertOneRecord")
        except pymysql.MySQLError as error4:
            # OM 2020.03.11 L'instruction suivante est indispensable pour annuler l'insertion des données (commande opposée : COMMIT)
            self.connection_dbc.db.rollback()
            print(" Il y a une MySQLError : %s", error4)
            print("connection_dbc.db.rollback() insertOneRecord")
        except pymysql.IntegrityError as error5:
            # OM 2020.03.11 L'instruction suivante est indispensable pour annuler l'insertion des données (commande opposée : COMMIT)
            self.connection_dbc.db.rollback()
            print(" Il y a une IntegrityError : %s", error5)
            print("connection_dbc.db.rollback() insertOneRecord")
        except:
            # OM 2020.03.11 L'instruction suivante est indispensable pour annuler l'insertion des données (commande opposée : COMMIT)
            self.connection_dbc.db.rollback()
            print("Unknown error occurred")
        finally:
            # On ferme le curseur et la base de donnée et on affiche un message dans la console.
            self.connection_dbc.DBcursor.close()
            self.connection_dbc.close_connection()
            print("DBcursor et DB fermés")


    def insert_one_record_many_values_one_table(self, requete_insert_mysql, valeurs_insertion):
        """
        Méthode qui permet d'insérer les valeurs passées en paramètres.
        OM 2020.03.24
                Parametres:
                        requete_insert_mysql (class 'str'): une classe string
                        valeurs_insertion (class 'dict'): une classe dictionnaire
                Retourne:
                        pas de valeurs
        """
        try:
            # OM 2020.01.28 CONNECTION A LA BD
            self.connection_dbc = connect_db.DatabaseTools()
            # Un simple test qui renvoie un message dans la console suivant l'état de la BD
            self.connection_dbc.is_connection_open()

            # Pour aider à comprendre les types de données on affiche dans la console.
            print("type >>> requete_insert_mysql ",type(requete_insert_mysql))
            print("type >>> valeurs_insertion ",type(valeurs_insertion))
            # Afficher les docstrings...très importantes pour votre projet.
            print(self.insert_one_record_many_values_one_table.__doc__)

            # OM 2020.03.11 Execute la requête avec un passage de paramètres
            self.connection_dbc.DBcursor.execute(requete_insert_mysql, valeurs_insertion)

            # OM 2020.03.11 L'instruction suivante est indispensable pour confirmer l'insertion des données (en cas de problèmes : rollback)
            self.connection_dbc.db.commit()

        except pymysql.Error as error:
            # OM 2020.03.11 L'instruction suivante est indispensable pour annuler l'insertion des données (commande opposée : COMMIT)
            self.connection_dbc.db.rollback()
            print(" Il y a une ERREUR : %s", error)
            print("connection_dbc.db.rollback() insertOneRecord")
        except pymysql.DataError as error1:
            # OM 2020.03.11 L'instruction suivante est indispensable pour annuler l'insertion des données (commande opposée : COMMIT)
            self.connection_dbc.db.rollback()
            print(" Il y a une DataError : %s", error1)
            print("connection_dbc.db.rollback() insertOneRecord")
        except pymysql.DatabaseError as error2:
            # OM 2020.03.11 L'instruction suivante est indispensable pour annuler l'insertion des données (commande opposée : COMMIT)
            self.connection_dbc.db.rollback()
            print(" Il y a une DatabaseError : %s", error2)
            print("connection_dbc.db.rollback() insertOneRecord")
        except pymysql.Warning as error3:
            # OM 2020.03.11 L'instruction suivante est indispensable pour annuler l'insertion des données (commande opposée : COMMIT)
            self.connection_dbc.db.rollback()
            print(" Il y a une Warning : %s", error3)
            print("connection_dbc.db.rollback() insertOneRecord")
        except pymysql.MySQLError as error4:
            # OM 2020.03.11 L'instruction suivante est indispensable pour annuler l'insertion des données (commande opposée : COMMIT)
            self.connection_dbc.db.rollback()
            print(" Il y a une MySQLError : %s", error4)
            print("connection_dbc.db.rollback() insertOneRecord")
        except pymysql.IntegrityError as error5:
            # OM 2020.03.11 L'instruction suivante est indispensable pour annuler l'insertion des données (commande opposée : COMMIT)
            self.connection_dbc.db.rollback()
            print(" Il y a une IntegrityError : %s", error5)
            print("connection_dbc.db.rollback() insertOneRecord")
        except:
            # OM 2020.03.11 L'instruction suivante est indispensable pour annuler l'insertion des données (commande opposée : COMMIT)
            self.connection_dbc.db.rollback()
            print("Unknown error occurred")
        finally:
            # On ferme le curseur et la base de donnée et on affiche un message dans la console.
            self.connection_dbc.DBcursor.close()
            self.connection_dbc.close_connection()
            print("DBcursor et DB fermés")