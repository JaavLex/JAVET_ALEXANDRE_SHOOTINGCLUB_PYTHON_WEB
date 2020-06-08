# data_gestion_concours_personne.py
# OM 2020.04.22 Permet de gérer (CRUD) les données de la table intermédiaire "t_concours_personne"

from flask import flash
from APP_SHOOTINGCLUB.DATABASE.connect_db_context_manager import MaBaseDeDonnee
from APP_SHOOTINGCLUB.DATABASE.erreurs import *


class Gestionconcourspersonne():
    def __init__ (self):
        try:
            # DEBUG bon marché : Pour afficher un message dans la console.
            print("dans le try de gestions concours")
            # OM 2020.04.11 La connexion à la base de données est-elle active ?
            # Renvoie une erreur si la connexion est perdue.
            MaBaseDeDonnee().connexion_bd.ping(False)
        except Exception as erreur:
            flash("Dans Gestion concours personne ...terrible erreur, il faut connecter une base de donnée", "danger")
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Exception grave Classe constructeur Gestionconcourspersonne {erreur.args[0]}")
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurConnexion(f"{msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[0]}")
        print("Classe constructeur Gestionconcourspersonne ")

    def concours_afficher_data (self):
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
            print(f"DGG gad pymysql errror {erreur.args[0]} {erreur.args[1]}")
            raise MaBdErreurPyMySl(
                f"DGG gad pymysql errror {msg_erreurs['ErreurPyMySql']['message']} {erreur.args[0]} {erreur.args[1]}")
        except Exception as erreur:
            print(f"DGG gad Exception {erreur.args}")
            raise MaBdErreurConnexion(f"DGG gad Exception {msg_erreurs['ErreurConnexionBD']['message']} {erreur.args}")
        except pymysql.err.IntegrityError as erreur:
            # OM 2020.04.09 On dérive "pymysql.err.IntegrityError" dans le fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurConnexion(f"DGG gad pei {msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[1]}")

    def concours_personne_afficher_data (self, valeur_id_personne_selected_dict):
        print("valeur_id_personne_selected_dict...", valeur_id_personne_selected_dict)
        try:

            # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # la commande MySql classique est "SELECT * FROM t_concours"
            # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
            # donc, je précise les champs à afficher

            strsql_personne_selected = """SELECT id_personne, nom_pers, prenom_pers, possession_arme, GROUP_CONCAT(id_concours) as concourspersonne FROM T_Concours_a_presence AS T1
                                        INNER JOIN T_Personne AS T2 ON T2.id_personne = T1.fk_personne
                                        INNER JOIN T_Concours AS T3 ON T3.id_concours = T1.fk_concours
                                        WHERE id_personne = %(value_id_personne_selected)s"""

            # strsql_concours_personne_non_attribues = """SELECT id_concours, date_concours, type_concours, nom_stand_de_tir, adresse_stand_de_tir FROM T_Concours AS T1
            #                                 INNER JOIN T_Type_concours AS FK1 ON T1.fk_type_concours = FK1.id_type_concours
            #                                 INNER JOIN T_Stand_de_tir AS FK2 ON T1.fk_stand_de_tir = FK2.id_stand_de_tir
            #                                 WHERE id_concours not in (SELECT id_concours as idconcourspersonne FROM T_Concours_a_presence AS T2
            #                                 INNER JOIN T_Personne AS T3 ON T3.id_personne = T2.fk_personne
            #                                 INNER JOIN T_Concours AS T4 ON T4.id_concours = T2.fk_concours
            #                                 WHERE id_personne = %(valeur_id_personne_selected_dict)s)"""

            strsql_concours_personne_non_attribues = """SELECT id_concours, date_concours FROM T_Concours
                                                        WHERE id_concours not in(SELECT id_concours as idconcourspersonne FROM T_Concours_a_presence AS T1
                                                        INNER JOIN T_Personne AS T2 ON T2.id_personne = T1.fk_personne
                                                        INNER JOIN T_Concours AS T3 ON T3.id_concours = T1.fk_concours
                                                        WHERE id_personne = %(value_id_personne_selected)s)"""

            # strsql_concours_personne_attribues = """SELECT id_personne, id_concours, date_concours, type_concours, nom_stand_de_tir, adresse_stand_de_tir FROM T_Concours_a_presence AS T1
            #                                 INNER JOIN T_Personne AS T2 ON T2.id_personne = T1.fk_personne
            #                                 INNER JOIN T_Concours AS T3 ON T3.id_concours = T1.fk_concours
            #                                 INNER JOIN T_Type_concours AS FK1 ON T3.fk_type_concours = FK1.id_type_concours
            #                                 INNER JOIN T_Stand_de_tir AS FK2 ON T3.fk_stand_de_tir = FK2.id_stand_de_tir
            #                                 WHERE id_personne = %(valeur_id_personne_selected_dict)s"""

            strsql_concours_personne_attribues = """SELECT id_personne, id_concours, date_concours FROM T_Concours_a_presence AS T1
                                                    INNER JOIN T_Personne AS T2 ON T2.id_personne = T1.fk_personne 
                                                    INNER JOIN T_Concours AS T3 ON T3.id_concours = T1.fk_concours
                                                    WHERE id_personne = %(value_id_personne_selected)s"""

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                # Envoi de la commande MySql
                mc_afficher.execute(strsql_concours_personne_non_attribues, valeur_id_personne_selected_dict)
                # Récupère les données de la requête.
                data_concours_personne_non_attribues = mc_afficher.fetchall()
                # Affichage dans la console
                print("dfad data_concours_personne_non_attribues ", data_concours_personne_non_attribues, " Type : ",
                      type(data_concours_personne_non_attribues))

                # Envoi de la commande MySql
                mc_afficher.execute(strsql_personne_selected, valeur_id_personne_selected_dict)
                # Récupère les données de la requête.
                data_personne_selected = mc_afficher.fetchall()
                # Affichage dans la console
                print("data_personne_selected  ", data_personne_selected, " Type : ", type(data_personne_selected))

                # Envoi de la commande MySql
                mc_afficher.execute(strsql_concours_personne_attribues, valeur_id_personne_selected_dict)
                # Récupère les données de la requête.
                data_concours_personne_attribues = mc_afficher.fetchall()
                # Affichage dans la console
                print("data_concours_personne_attribues ", data_concours_personne_attribues, " Type : ",
                      type(data_concours_personne_attribues))

                # Retourne les données du "SELECT"
                return data_personne_selected, data_concours_personne_non_attribues, data_concours_personne_attribues
        except pymysql.Error as erreur:
            print(f"DGGF gfad pymysql errror {erreur.args[0]} {erreur.args[1]}")
            raise MaBdErreurPyMySl(
                f"DGG gad pymysql errror {msg_erreurs['ErreurPyMySql']['message']} {erreur.args[0]} {erreur.args[1]}")
        except Exception as erreur:
            print(f"DGGF gfad Exception {erreur.args}")
            raise MaBdErreurConnexion(f"DGG gad Exception {msg_erreurs['ErreurConnexionBD']['message']} {erreur.args}")
        except pymysql.err.IntegrityError as erreur:
            # OM 2020.04.09 On dérive "pymysql.err.IntegrityError" dans le fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurConnexion(f"DGGF gfad pei {msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[1]}")

    def concours_personne_afficher_data_concat (self, id_personne_selected):
        print("id_personne_selected  ", id_personne_selected)
        try:
            # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # la commande MySql classique est "SELECT * FROM t_concours"
            # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
            # donc, je précise les champs à afficher

            strsql_concours_personne_afficher_data_concat = """SELECT id_personne, nom_pers, prenom_pers, possession_arme,
                                                            GROUP_CONCAT(date_concours) as concourspersonne FROM T_Concours_a_presence AS T1
                                                            RIGHT JOIN T_Personne AS T2 ON T2.id_personne = T1.fk_personne
                                                            LEFT JOIN T_Concours AS T3 ON T3.id_concours = T1.fk_concours
                                                            GROUP BY id_personne"""

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                # le paramètre 0 permet d'afficher tous les personne
                # Sinon le paramètre représente la valeur de l'id du personne
                if id_personne_selected == 0:
                    mc_afficher.execute(strsql_concours_personne_afficher_data_concat)
                else:
                    # Constitution d'un dictionnaire pour associer l'id du personne sélectionné avec un nom de variable
                    valeur_id_personne_selected_dictionnaire = {"value_id_personne_selected": id_personne_selected}
                    strsql_concours_personne_afficher_data_concat += """ HAVING id_personne= %(value_id_personne_selected)s"""
                    # Envoi de la commande MySql
                    mc_afficher.execute(strsql_concours_personne_afficher_data_concat, valeur_id_personne_selected_dictionnaire)

                # Récupère les données de la requête.
                data_concours_personne_afficher_concat = mc_afficher.fetchall()
                # Affichage dans la console
                print("dggf data_concours_personne_afficher_concat ", data_concours_personne_afficher_concat, " Type : ",
                      type(data_concours_personne_afficher_concat))

                # Retourne les données du "SELECT"
                return data_concours_personne_afficher_concat


        except pymysql.Error as erreur:
            print(f"DGGF gfadc pymysql errror {erreur.args[0]} {erreur.args[1]}")
            raise MaBdErreurPyMySl(
                f"DGG gad pymysql errror {msg_erreurs['ErreurPyMySql']['message']} {erreur.args[0]} {erreur.args[1]}")
        except Exception as erreur:
            print(f"DGGF gfadc Exception {erreur.args}")
            raise MaBdErreurConnexion(
                f"DGG gfadc Exception {msg_erreurs['ErreurConnexionBD']['message']} {erreur.args}")
        except pymysql.err.IntegrityError as erreur:
            # OM 2020.04.09 On dérive "pymysql.err.IntegrityError" dans le fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurConnexion(f"DGGF gfadc pei {msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[1]}")

    def concours_personne_add (self, valeurs_insertion_dictionnaire):
        try:
            print(valeurs_insertion_dictionnaire)
            # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # Insérer une (des) nouvelle(s) association(s) entre "id_personne" et "id_concours" dans la "t_concours_personne"
            strsql_insert_concours_personne = """INSERT INTO T_Concours_a_presence (id_concours_a_presence, fk_concours, fk_personne)
                                            VALUES (NULL, %(value_fk_concours)s, %(value_fk_personne)s)"""

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee() as mconn_bd:
                mconn_bd.mabd_execute(strsql_insert_concours_personne, valeurs_insertion_dictionnaire)


        except pymysql.err.IntegrityError as erreur:
            # OM 2020.04.09 On dérive "pymysql.err.IntegrityError" dans "MaBdErreurDoublon" fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurDoublon(
                f"DGG pei erreur doublon {msg_erreurs['ErreurDoublonValue']['message']} et son status {msg_erreurs['ErreurDoublonValue']['status']}")

    def concours_personne_delete (self, valeurs_insertion_dictionnaire):
        try:
            print(valeurs_insertion_dictionnaire)
            # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # Effacer une (des) association(s) existantes entre "id_personne" et "id_concours" dans la "t_concours_personne"
            strsql_delete_concours_personne = """DELETE FROM T_Concours_a_presence WHERE fk_concours = %(value_fk_concours)s AND fk_personne = %(value_fk_personne)s"""

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee() as mconn_bd:
                mconn_bd.mabd_execute(strsql_delete_concours_personne, valeurs_insertion_dictionnaire)
        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Problème concours_personne_delete Gestions concours personne numéro de l'erreur : {erreur}")
            # C'est une erreur à signaler à l'utilisateur de cette application WEB.
            flash(f"Flash. Problème concours_personne_delete Gestions concours personne  numéro de l'erreur : {erreur}", "danger")
            raise Exception(
                "Raise exception... Problème concours_personne_delete Gestions concours personne  {erreur}")

    def edit_concours_data (self, valeur_id_dictionnaire):
        try:
            print(valeur_id_dictionnaire)
            # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # Commande MySql pour afficher le concours sélectionné dans le tableau dans le formulaire HTML
            str_sql_id_concours = "SELECT id_concours, date_concours FROM T_Concours WHERE id_concours = %(value_id_concours)s"

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

    def update_concours_data (self, valeur_update_dictionnaire):
        try:
            print(valeur_update_dictionnaire)
            # OM 2019.04.02 Commande MySql pour la MODIFICATION de la valeur "CLAVIOTTEE" dans le champ "nameEditdateconcoursHTML" du form HTML "concoursEdit.html"
            # le "%s" permet d'éviter des injections SQL "simples"
            # <td><input type = "text" name = "nameEditdateconcoursHTML" value="{{ row.date_concours }}"/></td>
            str_sql_update_dateconcours = "UPDATE t_concours SET date_concours = %(value_name_concours)s WHERE id_concours = %(value_id_concours)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_update_dateconcours, valeur_update_dictionnaire)

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
                flash(f"Flash. Cette valeur existe déjà : {erreur}", "warning")
                # Deux façons de communiquer une erreur causée par l'insertion d'une valeur à double.
                flash(f"Doublon !!! Introduire une valeur différente", "warning")
                # Message en cas d'échec du bon déroulement des commandes ci-dessus.
                print(f"Problème update_concours_data Data Gestions concours numéro de l'erreur : {erreur}")

                raise Exception("Raise exception... Problème update_concours_data d'un concours DataGestionsconcours {erreur}")

    def delete_select_concours_data (self, valeur_delete_dictionnaire):
        try:
            print(valeur_delete_dictionnaire)
            # OM 2019.04.02 Commande MySql pour la MODIFICATION de la valeur "CLAVIOTTEE" dans le champ "nameEditdateconcoursHTML" du form HTML "concoursEdit.html"
            # le "%s" permet d'éviter des injections SQL "simples"
            # <td><input type = "text" name = "nameEditdateconcoursHTML" value="{{ row.date_concours }}"/></td>

            # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # Commande MySql pour afficher le concours sélectionné dans le tableau dans le formulaire HTML
            str_sql_select_id_concours = "SELECT id_concours, date_concours FROM T_Concours WHERE id_concours = %(value_id_concours)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode"mabd_execute" dans la classe "MaBaseDeDonnee"
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

    def delete_concours_data (self, valeur_delete_dictionnaire):
        try:
            print(valeur_delete_dictionnaire)
            # OM 2019.04.02 Commande MySql pour EFFACER la valeur sélectionnée par le "bouton" du form HTML "concoursEdit.html"
            # le "%s" permet d'éviter des injections SQL "simples"
            # <td><input type = "text" name = "nameEditdateconcoursHTML" value="{{ row.date_concours }}"/></td>
            str_sql_delete_dateconcours = "DELETE FROM T_Concours WHERE id_concours = %(value_id_concours)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_delete_dateconcours, valeur_delete_dictionnaire)
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
            flash(f"Flash. Problèmes Data Gestions concours numéro de l'erreur : {erreur}", "danger")
            if erreur.args[0] == 1451:
                # OM 2020.04.09 Traitement spécifique de l'erreur 1451 Cannot delete or update a parent row: a foreign key constraint fails
                # en MySql le moteur INNODB empêche d'effacer un concours qui est associé à un personne dans la table intermédiaire "t_concours_personne"
                # il y a une contrainte sur les FK de la table intermédiaire "t_concours_personne"
                # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                flash(f"Flash. IMPOSSIBLE d'effacer !!! Ce concours est associé à des personne dans la t_concours_personne !!! : {erreur}", "danger")
                # DEBUG bon marché : Pour afficher un message dans la console.
                print(f"IMPOSSIBLE d'effacer !!! Ce concours est associé à des personne dans la t_concours_personne !!! : {erreur}")
            raise MaBdErreurDelete(f"DGG Exception {msg_erreurs['ErreurDeleteContrainte']['message']} {erreur}")
