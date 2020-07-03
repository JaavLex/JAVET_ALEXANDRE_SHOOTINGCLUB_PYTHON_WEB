# routes_gestion_concours.py
# OM 2020.04.06 Gestions des "routes" FLASK pour les concours.

import pymysql
from flask import render_template, flash, redirect, url_for, request
from APP_SHOOTINGCLUB import obj_mon_application
from APP_SHOOTINGCLUB.CONCOURS.data_gestion_concours import GestionConcours
from APP_SHOOTINGCLUB.DATABASE.erreurs import *
import re

# OM 2020.04.16 Afficher un avertissement sympa...mais contraignant
# Pour la tester http://127.0.0.1:1234/avertissement_sympa_pour_geeks
@obj_mon_application.route("/avertissement_sympa_pour_geeks")
def avertissement_sympa_pour_geeks():
    # OM 2020.04.07 Envoie la page "HTML" au serveur.
    return render_template("concours/AVERTISSEMENT_SYMPA_POUR_LES_GEEKS_concours.html")




# # OM 2020.04.16 Afficher les concours
# # Pour la tester http://127.0.0.1:1234/concours_afficher
# @obj_mon_application.route("/concours_afficher")
# def concours_afficher():
#     # OM 2020.04.09 Pour savoir si les données d'un formulaire sont un affichage
#     # ou un envoi de donnée par des champs du formulaire HTML.
#     if request.method == "GET":
#         try:
#             # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
#             obj_actions_concours = GestionConcours()
#             # Récupére les données grâce à une requête MySql définie dans la classe GestionConcours()
#             # Fichier data_gestion_concours.py
#             data_concours = obj_actions_concours.concours_afficher_data()
#             # DEBUG bon marché : Pour afficher un message dans la console.
#             print(" data concours", data_concours, "type ", type(data_concours))
#
#             # OM 2020.04.09 La ligns ci-après permet de donner un sentiment rassurant aux utilisateurs.
#             flash("Données concours affichées !!", "Success")
#         except Exception as erreur:
#             print(f"RGF Erreur générale.")
#             # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
#             # Ainsi on peut avoir un message d'erreur personnalisé.
#             # flash(f"RGG Exception {erreur}")
#             raise Exception(f"RGF Erreur générale. {erreur}")
#
#     # OM 2020.04.07 Envoie la page "HTML" au serveur.
#     return render_template("concours/concours_afficher.html", data=data_concours)


@obj_mon_application.route("/concours_afficher/<string:order_by>/<int:id_concours_sel>", methods=['GET', 'POST'])
def concours_afficher(order_by,id_concours_sel):
    # OM 2020.04.09 Pour savoir si les données d'un formulaire sont un affichage
    # ou un envoi de donnée par des champs du formulaire HTML.
    if request.method == "GET":
        try:
            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_concours = GestionConcours()
            # Récupère les données grâce à une requête MySql définie dans la classe Gestionconcours()
            # Fichier data_gestion_concours.py
            # "order_by" permet de choisir l'ordre d'affichage des concours.
            data_concours = obj_actions_concours.concours_afficher_data(order_by,id_concours_sel)
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(" data concours", data_concours, "type ", type(data_concours))

            # Différencier les messages si la table est vide.
            if not data_concours and id_concours_sel == 0:
                flash("""La table "t_concours" est vide. !!""", "warning")
            elif not data_concours and id_concours_sel > 0:
                # Si l'utilisateur change l'id_concours dans l'URL et que le concours n'existe pas,
                flash(f"Le concours demandé n'existe pas !!", "warning")
            else:
                # Dans tous les autres cas, c'est que la table "t_concours" est vide.
                # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données concours affichés !!", "success")


        except Exception as erreur:
            print(f"RGG Erreur générale.")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # flash(f"RGG Exception {erreur}")
            raise Exception(f"RGG Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # OM 2020.04.07 Envoie la page "HTML" au serveur.
    return render_template("concours/concours_afficher.html", data=data_concours)



# OM 2020.04.06 Pour une simple démo. On insère deux fois des valeurs dans la table concours
# Une fois de manière fixe, vous devez changer les valeurs pour voir le résultat dans la table "t_concours"
# La 2ème il faut entrer la valeur du titre du film par le clavier, il ne doit pas être vide.
# Pour les autres valeurs elles doivent être changées ci-dessous.
# Une des valeurs est "None" ce qui en MySql donne "NULL" pour l'attribut "t_concours.cover_link_film"
# Pour la tester http://127.0.0.1:1234/concours_add
@obj_mon_application.route("/concours_add", methods=['GET', 'POST'])
def concours_add():
    # OM 2019.03.25 Pour savoir si les données d'un formulaire sont un affichage
    # ou un envoi de donnée par des champs utilisateurs.
    if request.method == "POST":
        try:
            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_concours = GestionConcours()
            # OM 2020.04.09 Récupère le contenu du champ dans le formulaire HTML "concours_add.html"
            date_concours_add = request.form['date_concours_html']
            type_concours_add = request.form['type_concours_html']
            stand_de_tir_add = request.form['stand_de_tir_html']

            # OM 2019.04.04 On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
            # des valeurs avec des caractères qui ne sont pas des lettres.
            # Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
            if not re.match("",
                                date_concours_add):
                # OM 2019.03.28 Message humiliant à l'attention de l'utilisateur.
                flash(f"Une entrée...incorrecte !! Pas de chiffres, de caractères spéciaux, d'espace à double, "
                      f"de double apostrophe, de double trait union et ne doit pas être vide.", "Danger")
                # On doit afficher à nouveau le formulaire "concours_add.html" à cause des erreurs de "claviotage"
                return render_template("concours/concours_add.html")
            else:

                # Constitution d'un dictionnaire et insertion dans la BD
                valeurs_insertion_dictionnaire = {"value_date_concours": date_concours_add, "value_fk_type_concours": type_concours_add, "value_fk_stand_de_tir": stand_de_tir_add}
                obj_actions_concours.add_concours_data(valeurs_insertion_dictionnaire)

                # OM 2019.03.25 Les 2 lignes ci-après permettent de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données insérées !!", "Sucess")
                print(f"Données insérées !!")
                # On va interpréter la "route" 'concours_afficher', car l'utilisateur
                # doit voir le nouveau concours qu'il vient d'insérer.
                return redirect(url_for('concours_afficher', id_concours_sel=0, order_by="ASC"))

        # OM 2020.04.16 ATTENTION à l'ordre des excepts très important de respecter l'ordre.
        except pymysql.err.IntegrityError as erreur:
            # OM 2020.04.09 On dérive "pymysql.err.IntegrityError" dans "MaBdErreurDoublon" fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurDoublon(f"RGG pei {msg_erreurs['ErreurDoublonValue']['message']} et son status {msg_erreurs['ErreurDoublonValue']['status']}")

        # OM 2020.04.16 ATTENTION à l'ordre des excepts très important de respecter l'ordre.
        except (pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                TypeError) as erreur:
            flash(f"Autre erreur {erreur}")
            raise MonErreur(f"Autre erreur")

        except Exception as erreur:
            # OM 2020.04.09 On dérive "Exception" dans "MaBdErreurConnexion" fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurConnexion(f"RGG Exception {msg_erreurs['ErreurConnexionBD']['message']} et son status {msg_erreurs['ErreurConnexionBD']['status']}")

        # OM 2020.04.16 ATTENTION à l'ordre des excepts très important de respecter l'ordre.
    # OM 2020.04.07 Envoie la page "HTML" au serveur.
    return render_template("concours/concours_add.html")

@obj_mon_application.route('/concours_select_delete', methods=['POST', 'GET'])
def concours_select_delete():

    if request.method == 'GET':
        try:

            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_concours = GestionConcours()
            # OM 2019.04.04 Récupérer la valeur de "idconcoursDeleteHTML" du formulaire html "concoursDelete.html"
            id_concours_delete = request.args.get('id_concours_delete_html')

            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_delete_dictionnaire = {"value_id_concours": id_concours_delete}


            # OM 2019.04.02 La commande MySql est envoyée à la BD
            data_id_concours = obj_actions_concours.delete_select_concours_data(valeur_delete_dictionnaire)
            flash(f"EFFACER et c'est terminé pour cette \"POV\" valeur !!!")

        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:
            # Communiquer qu'une erreur est survenue.
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Erreur concours_delete {erreur.args[0], erreur.args[1]}")
            # C'est une erreur à signaler à l'utilisateur de cette application WEB.
            flash(f"Erreur concours_delete {erreur.args[0], erreur.args[1]}")

    # Envoie la page "HTML" au serveur.
    return render_template('concours/concours_delete.html', data=data_id_concours)


# ---------------------------------------------------------------------------------------------------
# OM 2019.04.02 Définition d'une "route" /concoursUpdate , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# Permettre à l'utilisateur de modifier un concours, et de filtrer son entrée grâce à des expressions régulières REGEXP
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/concours_delete', methods=['POST', 'GET'])
def concours_delete():

    # OM 2019.04.02 Pour savoir si les données d'un formulaire sont un affichage ou un envoi de donnée par des champs utilisateurs.
    if request.method == 'POST':
        try:
            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_concours = GestionConcours()
            # OM 2019.04.02 Récupérer la valeur de "id_concours" du formulaire html "concoursAfficher.html"
            id_concours_delete = request.form['id_concours_delete_html']
            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_delete_dictionnaire = {"value_id_concours": id_concours_delete}

            data_concours = obj_actions_concours.delete_concours_data(valeur_delete_dictionnaire)
            # OM 2019.04.02 On va afficher la liste des concours des concours
            # OM 2019.04.02 Envoie la page "HTML" au serveur. On passe un message d'information dans "message_html"

            # On affiche les concours
            return redirect(url_for('concours_afficher', order_by='ASC', id_concours_sel=0))



        except (pymysql.err.OperationalError, pymysql.ProgrammingError, pymysql.InternalError, pymysql.IntegrityError,
                TypeError) as erreur:
            # OM 2020.04.09 Traiter spécifiquement l'erreur MySql 1451
            # Cette erreur 1451, signifie qu'on veut effacer un "concours" de concours qui est associé dans "t_concours_concours".
            if erreur.args[0] == 1451:
                # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                flash('IMPOSSIBLE d\'effacer !!! Cette valeur est associée à des concours !')
                # DEBUG bon marché : Pour afficher un message dans la console.
                print(f"IMPOSSIBLE d'effacer !! Ce concours est associé à des concours dans la t_concours_concours !!! : {erreur}")
                # Afficher la liste des concours des concours
                return redirect(url_for('concours_afficher'))
            else:
                # Communiquer qu'une autre erreur que la 1062 est survenue.
                # DEBUG bon marché : Pour afficher un message dans la console.
                print(f"Erreur concours_delete {erreur.args[0], erreur.args[1]}")
                # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                flash(f"Erreur concours_delete {erreur.args[0], erreur.args[1]}")


            # OM 2019.04.02 Envoie la page "HTML" au serveur.
    return render_template('concours/concours_afficher.html', data=data_concours)

@obj_mon_application.route('/concours_edit', methods=['POST', 'GET'])
def concours_edit():
    # OM 2020.04.07 Les données sont affichées dans un formulaire, l'affichage de la sélection
    # d'une seule ligne choisie par le bouton "edit" dans le formulaire "concours_afficher.html"
    if request.method == 'GET':
        try:
            # Récupérer la valeur de "id_concours" du formulaire html "concours_afficher.html"
            # l'utilisateur clique sur le lien "edit" et on récupére la valeur de "id_concours"
            # grâce à la variable "id_concours_edit_html"
            # <a href="{{ url_for('concours_edit', id_concours_edit_html=row.id_concours) }}">Edit</a>
            id_concours_edit = request.values['id_concours_edit_html']

            # Pour afficher dans la console la valeur de "id_concours_edit", une façon simple de se rassurer,
            # sans utiliser le DEBUGGER
            print(id_concours_edit)

            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_select_dictionnaire = {"value_id_concours": id_concours_edit}

            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_concours = GestionConcours()

            # OM 2019.04.02 La commande MySql est envoyée à la BD
            data_id_concours = obj_actions_concours.edit_concours_data(valeur_select_dictionnaire)
            print("dataIdconcours ", data_id_concours, "type ", type(data_id_concours))
            # Message ci-après permettent de donner un sentiment rassurant aux utilisateurs.
            flash(f"Editer le concours d'un per !!!")

        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:

            # On indique un problème, mais on ne dit rien en ce qui concerne la résolution.
            print("Problème avec la BD ! : %s", erreur)
            # OM 2020.04.09 On dérive "Exception" dans "MaBdErreurConnexion" fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurConnexion(f"RGG Exception {msg_erreurs['ErreurConnexionBD']['message']}"
                                      f"et son status {msg_erreurs['ErreurConnexionBD']['status']}")

    return render_template("concours/concours_edit.html", data=data_id_concours)


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.07 Définition d'une "route" /concours_update , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# On change la valeur d'un concours de concours par la commande MySql "UPDATE"
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/concours_update', methods=['POST', 'GET'])
def concours_update():
    # DEBUG bon marché : Pour afficher les méthodes et autres de la classe "flask.request"
    print(dir(request))
    # OM 2020.04.07 Les données sont affichées dans un formulaire, l'affichage de la sélection
    # d'une seule ligne choisie par le bouton "edit" dans le formulaire "concours_afficher.html"
    # Une fois que l'utilisateur à modifié la valeur du concours alors il va appuyer sur le bouton "UPDATE"
    # donc en "POST"
    if request.method == 'POST':
        try:
            # DEBUG bon marché : Pour afficher les valeurs contenues dans le formulaire
            print("request.values ",request.values)

            # Récupérer la valeur de "id_concours" du formulaire html "concours_edit.html"
            # l'utilisateur clique sur le lien "edit" et on récupére la valeur de "id_concours"
            # grâce à la variable "id_concours_edit_html"
            # <a href="{{ url_for('concours_edit', id_concours_edit_html=row.id_concours) }}">Edit</a>
            id_concours_edit = request.values['id_concours_edit_html']
            date_concours_edit = request.values['date_concours_edit_html']
            type_concours_edit = request.values['type_concours_edit_html']
            stand_de_tir_edit = request.values['stand_de_tir_edit_html']

            # Récupère le contenu du champ "intitule_concours" dans le formulaire HTML "concoursEdit.html"

            valeur_edit_list = [{'value_id_concours': id_concours_edit, 'value_date_concours': date_concours_edit, 'value_type_concours': type_concours_edit, 'value_stand_de_tir': stand_de_tir_edit}]
            # On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
            # des valeurs avec des caractères qui ne sont pas des lettres.
            # Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
            if not re.match("(.*?)", date_concours_edit):
                # En cas d'erreur, conserve la saisie fausse, afin que l'utilisateur constate sa misérable faute
                # Récupère le contenu du champ "intitule_concours" dans le formulaire HTML "concoursEdit.html"
                #nom_pers = request.values['name_edit_intitule_concours_html']
                # Message humiliant à l'attention de l'utilisateur.
                flash(f"Une entrée...incorrecte !! Pas de chiffres, de caractères spéciaux, d'espace à double, "
                      f"de double apostrophe, de double trait union et ne doit pas être vide.", "Danger")

                # On doit afficher à nouveau le formulaire "concours_edit.html" à cause des erreurs de "claviotage"
                # Constitution d'une liste pour que le formulaire d'édition "concours_edit.html" affiche à nouveau
                # la possibilité de modifier l'entrée
                # Exemple d'une liste : [{'id_concours': 13, 'intitule_concours': 'philosophique'}]
                valeur_edit_list = [{'value_id_concours': id_concours_edit, 'value_date_concours': date_concours_edit, 'value_type_concours': type_concours_edit, 'value_stand_de_tir': stand_de_tir_edit}]

                # DEBUG bon marché :
                # Pour afficher le contenu et le type de valeurs passées au formulaire "concours_edit.html"
                print(valeur_edit_list, "type ..",  type(valeur_edit_list))
                return render_template('concours/concours_edit.html', data=valeur_edit_list)
            else:
                # Constitution d'un dictionnaire et insertion dans la BD
                valeur_update_dictionnaire = {'value_id_concours': id_concours_edit, 'value_date_concours': date_concours_edit, 'value_type_concours': type_concours_edit, 'value_stand_de_tir': stand_de_tir_edit}

                # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
                obj_actions_concours = GestionConcours()

                # La commande MySql est envoyée à la BD
                data_id_concours = obj_actions_concours.update_concours_data(valeur_update_dictionnaire)
                # DEBUG bon marché :
                print("dataIdconcours ", data_id_concours, "type ", type(data_id_concours))
                # Message ci-après permettent de donner un sentiment rassurant aux utilisateurs.
                flash(f"Editer le concours d'un per !!!")
                # On affiche les concours
                return redirect(url_for('concours_afficher'))

        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:

            print(erreur.args)
            flash(f"problème concours update{erreur.args[0]}")
            # En cas de problème, mais surtout en cas de non respect
            # des régles "REGEX" dans le champ "name_edit_intitule_concours_html" alors on renvoie le formulaire "EDIT"
            return render_template('concours/concours_edit.html', data=valeur_edit_list)

    return render_template("concours/concours_update.html")


