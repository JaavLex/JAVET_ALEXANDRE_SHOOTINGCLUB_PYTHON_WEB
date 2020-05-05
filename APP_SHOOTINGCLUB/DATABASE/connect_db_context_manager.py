# connect_db_context_manager.py
#
# OM 2020.04.05 Classe pour se connecter à la base de donnée.
#
# La notion en Python de "context manager" aide à simplifier le code.
# https://docs.python.org/3/library/stdtypes.html#typecontextmanager
# https://book.pythontips.com/en/latest/context_managers.html

# Le coeur du système pour la connexion à la BD
# Si on utilise MAMP il faut choisir import mysql.connector
# https://dev.mysql.com/downloads/connector/python/
import pymysql
from APP_SHOOTINGCLUB.DATABASE.erreurs import *
# Petits messages "flash", échange entre Python et Jinja dans une page en HTML
from flask import flash


class MaBaseDeDonnee():
    # Quand on instancie la classe il interprète le code __init__
    def __init__(self):
        self.host = 'localhost'
        self.port = 33060
        self.user = 'root'
        self.password = 'Pomme'
        self.db = "JAVET_ALEXANDRE_SHOOTINGCLUB_BD_104"

        self.connexion_bd = None
        try:
            # OM 2019.04.05 ON SE CONNECTE A LA BASE DE DONNEE
            # ATTENTION : LE MOT DE PASSE PEUT CHANGER SUIVANT LE SERVEUR MySql QUE VOUS CHOISSISSEZ !!! (Uwamp, Xampp, etc)
            # autocommit doit être à False, sa valeur est testée lors de la sortie de cette classe.
            self.connexion_bd = pymysql.connect(host=self.host,
                                                port=self.port,
                                                user=self.user,
                                                password=self.password,
                                                db=self.db,
                                                cursorclass=pymysql.cursors.DictCursor,
                                                autocommit=False)
            print("Avec CM BD  CONNECTEE, TOUT va BIEN !! Dans le constructeur")
            print("self.con....", dir(self.connexion_bd), "type of self.con : ", type(self.connexion_bd))

        # OM 2020.03.11 Il y a un problème avec la BD (non connectée, nom erronné, etc)
        #
        except (Exception,
                ConnectionRefusedError,
                pymysql.err.OperationalError,
                pymysql.err.DatabaseError) as erreur:
            # OM 2019.03.09 SI LA BD N'EST PAS CONNECTEE, ON ENVOIE AU TERMINAL DES MESSAGES POUR RASSURER L'UTILISATEUR.
            # Petits messages "flash", échange entre Python et Jinja dans une page en HTML
            flash(f"Flash....BD NON CONNECTEE. Erreur : {erreur.args[1]}", "danger")
            # raise, permet de "lever" une exception et de personnaliser la page d'erreur
            # voir fichier "run_mon_app.py"
            # Celle-ci est assez complète... mais il y a toujours mieux
            print("erreur...MaBaseDeDonnee.__init__ ",erreur.args[1])
            raise MaBdErreurConnexion(f"{msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[1]}")
        print("Avec CM BD  INIT !! ")

    # Après la méthode __init__ il passe à __enter__, c'est là qu'il faut surveiller le bon déroulement
    # des actions. en cas de problèmes il ne va pas dans la méthode __exit__
    def __enter__(self):
        return self


    # Méthode de sortie de la classe, c'est là que se trouve tout ce qui doit être fermé
    # Si un problème (une Exception est levéee avant (__init__ ou __enter__) cette méthode
    # n'est pas interpretée
    def __exit__(self, exc_type, exc_val, traceback):
        # La valeur des paramètres est "None" si tout s'est bien déroulé.
        print("exc_val ", exc_val)
        """
            Si la sortie se passe bien ==> commit. Si exception ==> rollback
            
            Tous les paramètres sont de valeur "None" s'il n'y a pas eu d'EXCEPTION.
            En Python "None" est défini par la valeur "False"
        """
        if exc_val is None:
            print("commit !! Dans le destructeur ")
            self.connexion_bd.commit()
        else:
            print("rollback !! Dans le destructeur ")
            self.connexion_bd.rollback()

        # Fermeture de la connexion à la base de donnée.
        self.connexion_bd.close()
        print("La BD est FERMEE !! Dans le destructeur")

    # OM 2020.04.10 Cette méthode est définie pour utiliser les "context manager"
    # Une fois l'interprétation de cette méthode terminée
    # le destructeur "__exit__" sera automatiquement interprété.
    # ainsi après avoir éxécuté la requête MySql on va faire un commit (enregistrer les modifications)
    # s'il n'y a pas erreur ou un rollback (retour en arrière) en cas d'erreur
    # et finalement fermer la connexion à la BD.
    def mabd_execute(self, sql, params=None):
        print("execute",sql," params", params)
        return self.connexion_bd.cursor().execute(sql, params or ())

    # OM 2020.04.10 Cette méthode est définie pour utiliser les "context manager"
    def mabd_fetchall(self):
        return self.connexion_bd.cursor().fetchall()

