# data_gestion_arme.py
# OM 2020.04.09 Permet de gérer (CRUD) les données de la table t_arme
from flask import flash

from APP_SHOOTINGCLUB.DATABASE.connect_db_context_manager import MaBaseDeDonnee
from APP_SHOOTINGCLUB.DATABASE.erreurs import *


class Gestionarme():
    def __init__(self):
        try:
            # DEBUG bon marché : Pour afficher un message dans la console.
            print("dans le try de gestions arme")
            # OM 2020.04.11 La connexion à la base de données est-elle active ?
            # Renvoie une erreur si la connexion est perdue.
            MaBaseDeDonnee().connexion_bd.ping(False)
        except Exception as erreur:
            flash("Dans Gestion arme ...terrible erreur, il faut connecter une base de donnée", "Danger")
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Exception grave Classe constructeur Gestionarme {erreur.args[0]}")
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurConnexion(f"{msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[0]}")
        print("Classe constructeur Gestionarme ")

    def arme_afficher_data(self):
        try:
            # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # la commande MySql classique est "SELECT * FROM t_arme"
            # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
            # donc, je précise les champs à afficher
            strsql_arme_afficher = """SELECT id_arme, nom_arme, calibre, type_arme FROM T_Armes AS T1
                                      INNER JOIN T_Munition AS FK1 ON T1.fk_munition = FK1.id_munition
                                      INNER JOIN T_Type_arme AS FK2 ON T1.fk_type_arme = FK2.id_type_arme
                                      ORDER BY id_arme ASC"""
            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                # Envoi de la commande MySql
                mc_afficher.execute(strsql_arme_afficher)
                # Récupère les données de la requête.
                data_arme = mc_afficher.fetchall()
                # Affichage dans la console
                print("data_arme ", data_arme, " Type : ", type(data_arme))
                # Retourne les données du "SELECT"
                return data_arme
        except pymysql.Error as erreur:
            print(f"DGG gad pymysql errror {erreur.args[0]} {erreur.args[1]}")
            raise  MaBdErreurPyMySl(f"DGG gad pymysql errror {msg_erreurs['ErreurPyMySql']['message']} {erreur.args[0]} {erreur.args[1]}")
        except Exception as erreur:
            print(f"DGG gad Exception {erreur.args}")
            raise MaBdErreurConnexion(f"DGG gad Exception {msg_erreurs['ErreurConnexionBD']['message']} {erreur.args}")
        except pymysql.err.IntegrityError as erreur:
            # OM 2020.04.09 On dérive "pymysql.err.IntegrityError" dans le fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurConnexion(f"DGG gad pei {msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[1]}")

    def add_arme_data(self, valeurs_insertion_dictionnaire):
        try:
            print(valeurs_insertion_dictionnaire)
            # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            strsql_insert_arme = """INSERT INTO T_Armes (id_arme, nom_arme, fk_munition, fk_type_arme) VALUES (NULL, %(value_nom_arme)s, %(value_fk_munition)s, %(value_fk_type_arme)s)"""
            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee() as mconn_bd:
                mconn_bd.mabd_execute(strsql_insert_arme, valeurs_insertion_dictionnaire)


        except pymysql.err.IntegrityError as erreur:
            # OM 2020.04.09 On dérive "pymysql.err.IntegrityError" dans "MaBdErreurDoublon" fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurDoublon(f"DGG pei erreur doublon {msg_erreurs['ErreurDoublonValue']['message']} et son status {msg_erreurs['ErreurDoublonValue']['status']}")



    def edit_arme_data(self, valeur_id_dictionnaire):
        try:
            print(valeur_id_dictionnaire)
            # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # Commande MySql pour afficher le arme sélectionné dans le tableau dans le formulaire HTML
            str_sql_id_arme = "SELECT id_arme, nom_arme, fk_munition, fk_type_arme FROM T_Armes WHERE id_arme = %(value_id_arme)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_id_arme, valeur_id_dictionnaire)
                    data_one = mc_cur.fetchall()
                    print("valeur_id_dictionnaire...", data_one)
                    return data_one

        except Exception as erreur:
            # OM 2020.03.01 Message en cas d'échec du bon déroulement des commandes ci-dessus.
            print(f"Problème edit_arme_data Data Gestions arme numéro de l'erreur : {erreur}")
            # flash(f"Flash. Problèmes Data Gestions arme numéro de l'erreur : {erreur}", "danger")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise Exception(
                "Raise exception... Problème edit_arme_data d'un arme Data Gestions arme {erreur}")

    def update_arme_data(self, valeur_update_dictionnaire):
        try:
            print(valeur_update_dictionnaire)
            # OM 2019.04.02 Commande MySql pour la MODIFICATION de la valeur "CLAVIOTTEE" dans le champ "nameEditIntitulearmeHTML" du form HTML "armeEdit.html"
            # le "%s" permet d'éviter des injections SQL "simples"
            # <td><input type = "text" name = "nameEditIntitulearmeHTML" value="{{ row.intitule_arme }}"/></td>
            str_sql_update_intitulearme = "UPDATE T_Armes SET nom_arme = %(value_nom_arme)s, fk_munition = %(value_fk_munition)s, fk_type_arme = %(value_type_arme)s WHERE id_arme = %(value_id_arme)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_update_intitulearme, valeur_update_dictionnaire)

        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:
            # OM 2020.03.01 Message en cas d'échec du bon déroulement des commandes ci-dessus.
            print(f"Problème update_arme_data Data Gestions arme numéro de l'erreur : {erreur}")
            # flash(f"Flash. Problèmes Data Gestions arme numéro de l'erreur : {erreur}", "danger")
            # raise Exception('Raise exception... Problème update_arme_data d\'un arme Data Gestions arme {}'.format(str(erreur)))
            if erreur.args[0] == 1062:
                flash(f"Flash. Cette valeur existe déjà : {erreur}", "danger")
                # Deux façons de communiquer une erreur causée par l'insertion d'une valeur à double.
                flash('Doublon !!! Introduire une valeur différente')
                # Message en cas d'échec du bon déroulement des commandes ci-dessus.
                print(f"Problème update_arme_data Data Gestions arme numéro de l'erreur : {erreur}")

                raise Exception("Raise exception... Problème update_arme_data d'un arme DataGestionsarme {erreur}")

    def delete_select_arme_data(self, valeur_delete_dictionnaire):
        try:
            print(valeur_delete_dictionnaire)
            # OM 2019.04.02 Commande MySql pour la MODIFICATION de la valeur "CLAVIOTTEE" dans le champ "nameEditIntitulearmeHTML" du form HTML "armeEdit.html"
            # le "%s" permet d'éviter des injections SQL "simples"
            # <td><input type = "text" name = "nameEditIntitulearmeHTML" value="{{ row.intitule_arme }}"/></td>

            # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # Commande MySql pour afficher le arme sélectionné dans le tableau dans le formulaire HTML
            str_sql_select_id_arme = "SELECT id_arme, nom_arme, fk_munition, fk_type_arme FROM T_Armes WHERE id_arme = %(value_id_arme)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une gméthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_select_id_arme, valeur_delete_dictionnaire)
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
            print(f"Problème delete_select_arme_data Gestions arme numéro de l'erreur : {erreur}")
            # C'est une erreur à signaler à l'utilisateur de cette application WEB.
            flash(f"Flash. Problème delete_select_arme_data numéro de l'erreur : {erreur}", "danger")
            raise Exception("Raise exception... Problème delete_select_arme_data d\'un arme Data Gestions arme {erreur}")


    def delete_arme_data(self, valeur_delete_dictionnaire):
        try:
            print(valeur_delete_dictionnaire)
            # OM 2019.04.02 Commande MySql pour EFFACER la valeur sélectionnée par le "bouton" du form HTML "armeEdit.html"
            # le "%s" permet d'éviter des injections SQL "simples"
            # <td><input type = "text" name = "nameEditIntitulearmeHTML" value="{{ row.intitule_arme }}"/></td>
            str_sql_delete_intitulearme = "DELETE FROM T_Armes WHERE id_arme = %(value_id_arme)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_delete_intitulearme, valeur_delete_dictionnaire)
                    data_one = mc_cur.fetchall()
                    print("valeur_id_dictionnaire...",data_one)
                    return data_one
        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Problème delete_arme_data Data Gestions arme numéro de l'erreur : {erreur}")
            # flash(f"Flash. Problèmes Data Gestions arme numéro de l'erreur : {erreur}", "danger")
            if erreur.args[0] == 1451:
                # OM 2020.04.09 Traitement spécifique de l'erreur 1451 Cannot delete or update a parent row: a foreign key constraint fails
                # en MySql le moteur INNODB empêche d'effacer un arme qui est associé à un film dans la table intermédiaire "t_arme_concours"
                # il y a une contrainte sur les FK de la table intermédiaire "t_arme_concours"
                # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                # flash(f"Flash. IMPOSSIBLE d'effacer !!! Ce arme est associé à des concours dans la t_arme_concours !!! : {erreur}", "danger")
                # DEBUG bon marché : Pour afficher un message dans la console.
                print(f"IMPOSSIBLE d'effacer !!! Ce arme est associé à des concours dans la t_arme_concours !!! : {erreur}")
            raise MaBdErreurDelete(f"DGG Exception {msg_erreurs['ErreurDeleteContrainte']['message']} {erreur}")