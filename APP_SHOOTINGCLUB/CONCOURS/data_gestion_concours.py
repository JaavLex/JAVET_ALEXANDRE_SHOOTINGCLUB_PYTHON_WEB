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
            print(f"Exception grave Classe constructeur Gestionconcours {erreur.args[0]}")
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
    def add_concours_data(self, valeurs_insertion_dictionnaire):
        try:
            # # Définitions d'un dictionnaire pour passer les valeurs en paramètres de façon un "peu" sécurisée dans la BD
            # valeurs_insertion_dictionnaire = {'value_nom_film': valeur_ins_1, 'value_duree_film': valeur_ins_2,
            #                                   'date_sortie_film': valeur_ins_3}
            # Rssure la concours qui dévelloppe que les valeurs à insérer sont bien à disposition.concours
            print(valeurs_insertion_dictionnaire)
            str_sql_insert = "INSERT INTO T_Concours (id_concours, date_concours, fk_type_concours, fk_stand_de_tir) " \
                             "VALUES (NULL, %(value_date_concours)s, %(value_fk_type_concours)s, " \
                             "%(value_fk_stand_de_tir)s)"
            with MaBaseDeDonnee() as ma_bd_curseur:
                # OM Méthode "execute" définie simplement pour raccourcir la ligne de code
                # ligne de code normale : ma_bd_moi.connexion_bd.cursor(str_sql_insert, valeurs_insertion_dictionnaire)
                ma_bd_curseur.mabd_execute(str_sql_insert, valeurs_insertion_dictionnaire)

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

    def delete_select_concours_data(self, valeur_delete_dictionnaire):
            try:
                print(valeur_delete_dictionnaire)
                # OM 2019.04.02 Commande MySql pour la MODIFICATION de la valeur "CLAVIOTTEE" dans le champ "nameEditIntituleconcoursHTML" du form HTML "concoursEdit.html"
                # le "%s" permet d'éviter des injections SQL "simples"
                # <td><input type = "text" name = "nameEditIntituleconcoursHTML" value="{{ row.intitule_concours }}"/></td>

                # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                # Commande MySql pour afficher le concours sélectionné dans le tableau dans le formulaire HTML
                str_sql_select_id_concours = """SELECT id_concours, date_concours, type_concours, nom_stand_de_tir, adresse_stand_de_tir FROM T_Concours AS T1 
            INNER JOIN T_Type_concours AS FK1 ON T1.fk_type_concours = FK1.id_type_concours 
            INNER JOIN T_Stand_de_tir AS FK2 ON T1.fk_stand_de_tir = FK2.id_stand_de_tir
            WHERE id_concours = %(value_id_concours)s"""

                # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
                # la subtilité consiste à avoir une gméthode "mabd_execute" dans la classe "MaBaseDeDonnee"
                # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
                # sera interprété, ainsi on fera automatiquement un commit
                with MaBaseDeDonnee().connexion_bd as mconn_bd:
                    with mconn_bd as mc_cur:
                        mc_cur.execute(str_sql_select_id_concours, valeur_delete_dictionnaire)
                        data_one = mc_cur.fetchall()
                        print("valeur_id_dictionnaire...", data_one)
                        return data_one

            except (Exception,
                    pymysql.err.OperationalError,
                    pymysql.ProgrammingError,
                    pymysql.InternalError,
                    pymysql.IntegrityError,
                    TypeError) as erreur:
                # DEBUG bon marché : Pour afficher un message dans la console.
                print(f"Problème delete_select_concours_data Gestions concours numéro de l'erreur : {erreur}")
                # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                flash(f"Flash. Problème delete_select_concours_data numéro de l'erreur : {erreur}", "danger")
                raise Exception(
                    "Raise exception... Problème delete_select_concours_data d\'un concours Data Gestions concours {erreur}")

    def delete_concours_data(self, valeur_delete_dictionnaire):
            try:
                print(valeur_delete_dictionnaire)
                # OM 2019.04.02 Commande MySql pour EFFACER la valeur sélectionnée par le "bouton" du form HTML "concoursEdit.html"
                # le "%s" permet d'éviter des injections SQL "simples"
                # <td><input type = "text" name = "nameEditIntituleconcoursHTML" value="{{ row.intitule_concours }}"/></td>
                str_sql_delete_intituleconcours = "DELETE FROM T_Concours WHERE id_concours = %(value_id_concours)s"

                # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
                # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
                # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
                # sera interprété, ainsi on fera automatiquement un commit
                with MaBaseDeDonnee().connexion_bd as mconn_bd:
                    with mconn_bd as mc_cur:
                        mc_cur.execute(str_sql_delete_intituleconcours, valeur_delete_dictionnaire)
                        data_one = mc_cur.fetchall()
                        print("valeur_id_dictionnaire...", data_one)
                        return data_one
            except (Exception,
                    pymysql.err.OperationalError,
                    pymysql.ProgrammingError,
                    pymysql.InternalError,
                    pymysql.IntegrityError,
                    TypeError) as erreur:
                # DEBUG bon marché : Pour afficher un message dans la console.
                print(f"Problème delete_concours_data Data Gestions concours numéro de l'erreur : {erreur}")
                # flash(f"Flash. Problèmes Data Gestions concours numéro de l'erreur : {erreur}", "danger")
                if erreur.args[0] == 1451:
                    # OM 2020.04.09 Traitement spécifique de l'erreur 1451 Cannot delete or update a parent row: a foreign key constraint fails
                    # en MySql le moteur INNODB empêche d'effacer un concours qui est associé à un film dans la table intermédiaire "t_concours_concours"
                    # il y a une contrainte sur les FK de la table intermédiaire "t_concours_concours"
                    # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                    # flash(f"Flash. IMPOSSIBLE d'effacer !!! Ce concours est associé à des concours dans la t_concours_concours !!! : {erreur}", "danger")
                    # DEBUG bon marché : Pour afficher un message dans la console.
                    print(
                        f"IMPOSSIBLE d'effacer !!! Ce concours est associé à des concours dans la t_concours_concours !!! : {erreur}")
                raise MaBdErreurDelete(f"DGG Exception {msg_erreurs['ErreurDeleteContrainte']['message']} {erreur}")

    def edit_concours_data(self, valeur_id_dictionnaire):
        try:
            print(valeur_id_dictionnaire)
            # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # Commande MySql pour afficher le concours sélectionné dans le tableau dans le formulaire HTML
            str_sql_id_concours = "SELECT id_concours, date_concours, fk_type_concours, fk_stand_de_tir FROM T_Concours WHERE id_concours = %(value_id_concours)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_id_concours, valeur_id_dictionnaire)
                    data_one = mc_cur.fetchall()
                    print("valeur_id_dictionnaire...", data_one)
                    return data_one

        except Exception as erreur:
            # OM 2020.03.01 Message en cas d'échec du bon déroulement des commandes ci-dessus.
            print(f"Problème edit_concours_data Data Gestions concours numéro de l'erreur : {erreur}")
            # flash(f"Flash. Problèmes Data Gestions concours numéro de l'erreur : {erreur}", "danger")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise Exception(
                "Raise exception... Problème edit_concours_data d'un concours Data Gestions concours {erreur}")

    def update_concours_data(self, valeur_update_dictionnaire):
        try:
            print(valeur_update_dictionnaire)
            # OM 2019.04.02 Commande MySql pour la MODIFICATION de la valeur "CLAVIOTTEE" dans le champ "nameEditIntituleconcoursHTML" du form HTML "concoursEdit.html"
            # le "%s" permet d'éviter des injections SQL "simples"
            # <td><input type = "text" name = "nameEditIntituleconcoursHTML" value="{{ row.intitule_concours }}"/></td>
            str_sql_update_intituleconcours = "UPDATE T_Concours SET date_concours = %(value_date_concours)s, fk_type_concours = %(value_type_concours)s, fk_stand_de_tir = %(value_stand_de_tir)s WHERE id_concours = %(value_id_concours)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_update_intituleconcours, valeur_update_dictionnaire)

        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:
            # OM 2020.03.01 Message en cas d'échec du bon déroulement des commandes ci-dessus.
            print(f"Problème update_concours_data Data Gestions concours numéro de l'erreur : {erreur}")
            # flash(f"Flash. Problèmes Data Gestions concours numéro de l'erreur : {erreur}", "danger")
            # raise Exception('Raise exception... Problème update_concours_data d\'un concours Data Gestions concours {}'.format(str(erreur)))
            if erreur.args[0] == 1062:
                flash(f"Flash. Cette valeur existe déjà : {erreur}", "danger")
                # Deux façons de communiquer une erreur causée par l'insertion d'une valeur à double.
                flash('Doublon !!! Introduire une valeur différente')
                # Message en cas d'échec du bon déroulement des commandes ci-dessus.
                print(f"Problème update_concours_data Data Gestions concours numéro de l'erreur : {erreur}")

                raise Exception("Raise exception... Problème update_concours_data d'un concours DataGestionsconcours {erreur}")
