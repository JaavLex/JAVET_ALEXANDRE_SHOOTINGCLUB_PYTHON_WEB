# connect_db.py
# OM 2020.03.12 Connexion bd

import pymysql
import pymysql.cursors

# OM 2020.03.16 Se connecter à la BD.
class DatabaseTools():
    def __init__(self):
        print("Constructeur classe DatabaseTools ")

        try:
            # OM 2019.03.09 ON SE CONNECTE A LA BASE DE DONNEE
            # ATTENTION : LE MOT DE PASSE PEUT CHANGER SUIVANT LE SERVEUR MySql QUE VOUS CHOISSISSEZ !!! (Uwamp, Xampp, etc)
            self.db = pymysql.connect(host='localhost',
                                      port=33060,
                                      user="root",
                                      password="Pomme",
                                      db="JAVET_ALEXANDRE_SHOOTINGCLUB_BD_104",
                                      cursorclass=pymysql.cursors.DictCursor)
            print("Successfully connected to DataBase")
            # un curseur est directement à disposition, il faudra le fermer une fois que les actions sont réalisées
            self.DBcursor = self.db.cursor()

        # OM 2020.03.11 Si il y a un problème avec la BD (non connectée, nom erronné, etc) on peut envoyer un message plus précis que le précédent
        except pymysql.DatabaseError as error:
            # OM 2019.03.09 SI LA BD N'EST PAS CONNECTEE, ON ENVOIE AU TERMINAL DES MESSAGES POUR RASSURER L'UTILISATEUR.
            # Plusieurs façons d'envoyer des messages d'erreurs à la console
            print("BD NON CONNECTEE, numéro de l'erreur : %s", error)
            print("Exception number: {}, value {!r}".format(error.args[0], error))
            raise ValueError(f"Impossible de connecter la base de donnée\n{error}") from None
            self.mon_curseur_db.close()
        # OM 2020.03.11 La difficulté est de pièger, de traquer la moindre erreur du système. C'est une initiation donc je ne serai jamais responsable
        # d'une vraie mise en situation dans le monde réel de la terre de l'univers du monde entier
        # On ne peut pas tenir compte de la "CORONAPANIC"
        except (pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                pymysql.NotSupportedError,
                pymysql.Error,
                pymysql.DataError) as error:
            print("Il y a une ERREUR : %s", error)
            raise ValueError(f"Impossible de connecter la BD\n{error}") from None
            self.mon_curseur_db.close()

    # OM 2020.03.11 Petite méthode pour fermer la connection à la BD
    def close_connection(self):
        if self.db.open:
            print("Dans la méthode close_connection et la BD est FERMEE")
            self.db.close()
        else:
            print("Dans la méthode close_connection et y'a rien a fermer")

    # OM 2020.03.11 Petite méthode pour TESTER l'état de la connection à la BD
    def is_connection_open(self):
        if self.db.open:
            print("Dans la méthode is_connection_open la BD est OUVERTE")
            return True
        else:
            print("Dans la méthode is_connection_open et y'a rien à fermer")
            return False