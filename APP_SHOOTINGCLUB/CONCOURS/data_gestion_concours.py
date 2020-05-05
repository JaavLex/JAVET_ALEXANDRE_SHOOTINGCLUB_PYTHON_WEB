# data_gestion_concours.py
# OM 2698.03.21 Permet de gérer (CRUD) les données de la table t_concours


from flask import flash

from APP_SHOOTINGCLUB.DATABASE import connect_db_context_manager
from APP_SHOOTINGCLUB import obj_mon_application
from APP_SHOOTINGCLUB.DATABASE.connect_db_context_manager import MaBaseDeDonnee
from APP_SHOOTINGCLUB.DATABASE.erreurs import *



class GestionConcours():
    def __init__(self):
        try:
            print("dans le try de gestions concours")
            # OM 2020.04.11 La connexion à la base de données est-elle active ?
            # Renvoie une erreur si la connexion est perdue.
            MaBaseDeDonnee().connexion_bd.ping(False)
        except Exception as erreur:
            flash("Dans Gestion concours ...terrible erreur, il faut connecter une base de donnée", "Danger")
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Exception grave Classe constructeur GestionPersonne {erreur.args[0]}")
            raise MaBdErreurConnexion(f"{msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[0]}")

        print("Classe constructeur Gestionconcours ")


    def concours_afficher_data(self):
        try:
            # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # la commande MySql classique est "SELECT * FROM t_concours"
            # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
            # donc, je précise les champs à afficher
            strsql_concours_afficher = """SELECT id_concours, date_concours, type_concours, nom_stand_de_tir, adresse_stand_de_tir FROM T_Concours AS T1 
            INNER JOIN T_Type_concours AS FK1 ON T1.fk_type_concours = FK1.id_type_concours 
            INNER JOIN T_Stand_de_tir AS FK2 ON T1.fk_stand_de_tir = FK2.id_stand_de_tir"""
            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                # Envoi de la commande MySql
                mc_afficher.execute(strsql_concours_afficher)
                # Récupère les données de la requête.
                data_concours = mc_afficher.fetchall()
                # Affichage dans la console
                print("data_concours ", data_concours, " Type : ", type(data_concours))
                # Retourne les données du "SELECT"
                return data_concours
        except pymysql.Error as erreur:
            print(f"DGF gad pymysql errror {erreur.args[0]} {erreur.args[1]}")
            raise  MaBdErreurPyMySl(f"DGG fad pymysql errror {msg_erreurs['ErreurPyMySql']['message']} {erreur.args[0]} {erreur.args[1]}")
        except Exception as erreur:
            print(f"DGF gad Exception {erreur.args}")
            raise MaBdErreurConnexion(f"DGG fad Exception {msg_erreurs['ErreurConnexionBD']['message']} {erreur.args}")
        except pymysql.err.IntegrityError as erreur:
            # OM 2020.04.09 On dérive "pymysql.err.IntegrityError" dans "MaBdErreurDoublon" fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # raise MaBdErreurDoublon(f"{msg_erreurs['ErreurDoublonValue']['message']} et son status {msg_erreurs['ErreurDoublonValue']['status']}")
            raise MaBdErreurConnexion(f"DGF fad pei {msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[1]}")



    # def add_film(self, nom_film, duree_film, date_sortie_film):
    def add_film(self, valeurs_insertion_dictionnaire):
        try:
            # # Définitions d'un dictionnaire pour passer les valeurs en paramètres de façon un "peu" sécurisée dans la BD
            # valeurs_insertion_dictionnaire = {'value_nom_film': valeur_ins_1, 'value_duree_film': valeur_ins_2,
            #                                   'date_sortie_film': valeur_ins_3}
            # Rssure la personne qui dévelloppe que les valeurs à insérer sont bien à disposition.concours
            print(valeurs_insertion_dictionnaire)
            str_sql_insert = "INSERT INTO T_Concours (id_concours, date_concours, fk_type_concours, fk_stand_de_tir) " \
                             "VALUES (NULL, %(value_date_concours)s, %(value_fk_type_concours)s, " \
                             "%(value_fk_stand_de_tir)s)"
            with MaBaseDeDonnee() as ma_bd_curseur:
                # OM Méthode "execute" définie simplement pour raccourcir la ligne de code
                # ligne de code normale : ma_bd_moi.connexion_bd.cursor(str_sql_insert, valeurs_insertion_dictionnaire)
                ma_bd_curseur.execute(str_sql_insert, valeurs_insertion_dictionnaire)

        except Exception as erreur:
            # OM 2020.04.09 DIFFERENTS MOYENS D'INFORMER EN CAS D'ERREURS.
            # Message dans la console en cas d'échec du bon déroulement des commandes ci-dessus.
            print("Data Gestions concours ERREUR: {0}".format(erreur))
            print(f"Print console ... Data Gestions concours, numéro de l'erreur : {erreur}")
            # Petits messages "flash", échange entre Python et Jinja dans une page en HTML
            flash(f"Flash ... Data Gestions concours, numéro de l'erreur : {erreur}")
            # raise, permet de "lever" une exception et de personnaliser la page d'erreur
            # voir fichier "run_mon_app.py"

            print("erreur args.. ",erreur.args)
            code, msg = erreur.args
            print(" codes d'erreurs ---> ", error_codes.get(code, msg))
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise Exception(f"Raise exception... Data Gestions concours {erreur}")