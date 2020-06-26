# routes_gestion_arme.py
# OM 2020.04.06 Gestions des "routes" FLASK pour les arme.

from flask import render_template, flash, redirect, url_for, request
from APP_SHOOTINGCLUB import obj_mon_application
from APP_SHOOTINGCLUB.ARME.data_gestion_arme import Gestionarme
from APP_SHOOTINGCLUB.DATABASE.erreurs import *
# OM 2020.04.10 Pour utiliser les expressions régulières REGEX
import re


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.07 Définition d'une "route" /arme_afficher
# cela va permettre de programmer les actions avant d'interagir
# avec le navigateur par la méthode "render_template"
# Pour tester http://127.0.0.1:1234/arme<td>{{ row.nom_pers }}</td>_afficher
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/arme_afficher", methods=['GET', 'POST'])
def arme_afficher():
    # OM 2020.04.09 Pour savoir si les données d'un formulaire sont un affichage
    # ou un envoi de donnée par des champs du formulaire HTML.
    if request.method == "GET":
        try:
            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_arme = Gestionarme()
            # Récupére les données grâce à une requête MySql définie dans la classe Gestionarme()
            # Fichier data_gestion_arme.py
            data_arme = obj_actions_arme.arme_afficher_data()
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(" data arme", data_arme, "type ", type(data_arme))

            # OM 2020.04.09 La ligns ci-après permet de donner un sentiment rassurant aux utilisateurs.
            flash("Données arme affichées !!", "Success")
        except Exception as erreur:
            print(f"RGG Erreur générale.")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # flash(f"RGG Exception {erreur}")
            raise Exception(f"RGG Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # OM 2020.04.07 Envoie la page "HTML" au serveur.
    return render_template("arme/arme_afficher.html", data=data_arme)


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.07 Définition d'une "route" /arme_add ,
# cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template"
# En cas d'erreur on affiche à nouveau la page "arme_add.html"
# Pour la tester http://127.0.0.1:1234/arme_add
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/arme_add", methods=['GET', 'POST'])
def arme_add():
    # OM 2019.03.25 Pour savoir si les données d'un formulaire sont un affichage
    # ou un envoi de donnée par des champs utilisateurs.
    if request.method == "POST":
        try:
            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_arme = Gestionarme()
            # OM 2020.04.09 Récupère le contenu du champ dans le formulaire HTML "arme_add.html"
            nom_arme_add = request.form['nom_arme_html']
            fk_munition_add = request.form['fk_munition_html']
            fk_type_arme_add = request.form['fk_type_arme_html']

            # OM 2019.04.04 On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
            # des valeurs avec des caractères qui ne sont pas des lettres.
            # Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
            if not re.match("^([A-Z]|[a-z\u00C0-\u00FF])[A-Za-z\u00C0-\u00FF]*['\\- ]?[A-Za-z\u00C0-\u00FF]+$",
                                nom_arme_add):
                # OM 2019.03.28 Message humiliant à l'attention de l'utilisateur.
                flash(f"Une entrée...incorrecte !! Pas de chiffres, de caractères spéciaux, d'espace à double, "
                      f"de double apostrophe, de double trait union et ne doit pas être vide.", "Danger")
                # On doit afficher à nouveau le formulaire "arme_add.html" à cause des erreurs de "claviotage"
                return render_template("arme/arme_add.html")
            else:

                # Constitution d'un dictionnaire et insertion dans la BD
                valeurs_insertion_dictionnaire = {"value_nom_arme": nom_arme_add, "value_fk_munition": fk_munition_add, "value_fk_type_arme": fk_type_arme_add}
                obj_actions_arme.add_arme_data(valeurs_insertion_dictionnaire)

                # OM 2019.03.25 Les 2 lignes ci-après permettent de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données insérées !!", "Sucess")
                print(f"Données insérées !!")
                # On va interpréter la "route" 'arme_afficher', car l'utilisateur
                # doit voir le nouveau arme qu'il vient d'insérer.
                return redirect(url_for('arme_afficher'))

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

        # OM 2020.04.16 ATTENTION à l'ordre des excepts très important de respecter l'ordre.
        except Exception as erreur:
            # OM 2020.04.09 On dérive "Exception" dans "MaBdErreurConnexion" fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurConnexion(f"RGG Exception {msg_erreurs['ErreurConnexionBD']['message']} et son status {msg_erreurs['ErreurConnexionBD']['status']}")
    # OM 2020.04.07 Envoie la page "HTML" au serveur.
    return render_template("arme/arme_add.html")


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.07 Définition d'une "route" /arme_edit , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# On change la valeur d'un arme de concours par la commande MySql "UPDATE"
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/arme_edit', methods=['POST', 'GET'])
def arme_edit():
    # OM 2020.04.07 Les données sont affichées dans un formulaire, l'affichage de la sélection
    # d'une seule ligne choisie par le bouton "edit" dans le formulaire "arme_afficher.html"
    if request.method == 'GET':
        try:
            # Récupérer la valeur de "id_arme" du formulaire html "arme_afficher.html"
            # l'utilisateur clique sur le lien "edit" et on récupére la valeur de "id_arme"
            # grâce à la variable "id_arme_edit_html"
            # <a href="{{ url_for('arme_edit', id_arme_edit_html=row.id_arme) }}">Edit</a>
            id_arme_edit = request.values['id_arme_edit_html']

            # Pour afficher dans la console la valeur de "id_arme_edit", une façon simple de se rassurer,
            # sans utiliser le DEBUGGER
            print(id_arme_edit)

            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_select_dictionnaire = {"value_id_arme": id_arme_edit}

            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_arme = Gestionarme()

            # OM 2019.04.02 La commande MySql est envoyée à la BD
            data_id_arme = obj_actions_arme.edit_arme_data(valeur_select_dictionnaire)
            print("dataIdarme ", data_id_arme, "type ", type(data_id_arme))
            # Message ci-après permettent de donner un sentiment rassurant aux utilisateurs.
            flash(f"Editer le arme d'un per !!!")

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

    return render_template("arme/arme_edit.html", data=data_id_arme)


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.07 Définition d'une "route" /arme_update , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# On change la valeur d'un arme de concours par la commande MySql "UPDATE"
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/arme_update', methods=['POST', 'GET'])
def arme_update():
    # DEBUG bon marché : Pour afficher les méthodes et autres de la classe "flask.request"
    print(dir(request))
    # OM 2020.04.07 Les données sont affichées dans un formulaire, l'affichage de la sélection
    # d'une seule ligne choisie par le bouton "edit" dans le formulaire "arme_afficher.html"
    # Une fois que l'utilisateur à modifié la valeur du arme alors il va appuyer sur le bouton "UPDATE"
    # donc en "POST"
    if request.method == 'POST':
        try:
            # DEBUG bon marché : Pour afficher les valeurs contenues dans le formulaire
            print("request.values ",request.values)

            # Récupérer la valeur de "id_arme" du formulaire html "arme_edit.html"
            # l'utilisateur clique sur le lien "edit" et on récupére la valeur de "id_arme"
            # grâce à la variable "id_arme_edit_html"
            # <a href="{{ url_for('arme_edit', id_arme_edit_html=row.id_arme) }}">Edit</a>
            id_arme_edit = request.values['id_arme_edit_html']
            nom_arme_edit = request.values['nom_arme_html']
            fk_munition_edit = request.values['fk_munition_html']
            fk_type_arme_edit = request.values['fk_type_arme_html']

            # Récupère le contenu du champ "intitule_arme" dans le formulaire HTML "armeEdit.html"

            valeur_edit_list = [{'id_arme': id_arme_edit, 'nom_arme': nom_arme_edit, 'fk_munition': fk_munition_edit, 'fk_type_arme': fk_type_arme_edit}]
            # On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
            # des valeurs avec des caractères qui ne sont pas des lettres.
            # Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
            if not re.match("^([A-Z]|[a-z\u00C0-\u00FF])[A-Za-z\u00C0-\u00FF]*['\\- ]?[A-Za-z\u00C0-\u00FF]+$", nom_arme_edit):
                # En cas d'erreur, conserve la saisie fausse, afin que l'utilisateur constate sa misérable faute
                # Récupère le contenu du champ "intitule_arme" dans le formulaire HTML "armeEdit.html"
                #nom_pers = request.values['name_edit_intitule_arme_html']
                # Message humiliant à l'attention de l'utilisateur.
                flash(f"Une entrée...incorrecte !! Pas de chiffres, de caractères spéciaux, d'espace à double, "
                      f"de double apostrophe, de double trait union et ne doit pas être vide.", "Danger")

                # On doit afficher à nouveau le formulaire "arme_edit.html" à cause des erreurs de "claviotage"
                # Constitution d'une liste pour que le formulaire d'édition "arme_edit.html" affiche à nouveau
                # la possibilité de modifier l'entrée
                # Exemple d'une liste : [{'id_arme': 13, 'intitule_arme': 'philosophique'}]
                valeur_edit_list = [{'id_arme': id_arme_edit, 'nom_arme': nom_arme_edit, 'fk_munition': fk_munition_edit, 'fk_type_arme': fk_type_arme_edit}]

                # DEBUG bon marché :
                # Pour afficher le contenu et le type de valeurs passées au formulaire "arme_edit.html"
                print(valeur_edit_list, "type ..",  type(valeur_edit_list))
                return render_template('arme/arme_edit.html', data=valeur_edit_list)
            else:
                # Constitution d'un dictionnaire et insertion dans la BD
                valeur_update_dictionnaire = {"value_id_arme": id_arme_edit, "value_nom_arme": nom_arme_edit, "value_fk_munition": fk_munition_edit, "value_fk_type_arme": fk_type_arme_edit}

                # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
                obj_actions_arme = Gestionarme()

                # La commande MySql est envoyée à la BD
                data_id_arme = obj_actions_arme.update_arme_data(valeur_update_dictionnaire)
                # DEBUG bon marché :
                print("dataIdarme ", data_id_arme, "type ", type(data_id_arme))
                # Message ci-après permettent de donner un sentiment rassurant aux utilisateurs.
                flash(f"Editer le arme d'un per !!!")
                # On affiche les arme
                return redirect(url_for('arme_afficher'))

        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:

            print(erreur.args)
            flash(f"problème arme update{erreur.args[0]}")
            # En cas de problème, mais surtout en cas de non respect
            # des régles "REGEX" dans le champ "name_edit_intitule_arme_html" alors on renvoie le formulaire "EDIT"
            return render_template('arme/arme_edit.html', data=valeur_edit_list)

    return render_template("arme/arme_update.html")


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.07 Définition d'une "route" /arme_select_delete , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# On change la valeur d'un arme de concours par la commande MySql "UPDATE"
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/arme_select_delete', methods=['POST', 'GET'])
def arme_select_delete():

    if request.method == 'GET':
        try:

            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_arme = Gestionarme()
            # OM 2019.04.04 Récupérer la valeur de "idarmeDeleteHTML" du formulaire html "armeDelete.html"
            id_arme_delete = request.args.get('id_arme_delete_html')

            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_delete_dictionnaire = {"value_id_arme": id_arme_delete}


            # OM 2019.04.02 La commande MySql est envoyée à la BD
            data_id_arme = obj_actions_arme.delete_select_arme_data(valeur_delete_dictionnaire)
            flash(f"EFFACER et c'est terminé pour cette \"POV\" valeur !!!")

        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:
            # Communiquer qu'une erreur est survenue.
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Erreur arme_delete {erreur.args[0], erreur.args[1]}")
            # C'est une erreur à signaler à l'utilisateur de cette application WEB.
            flash(f"Erreur arme_delete {erreur.args[0], erreur.args[1]}")

    # Envoie la page "HTML" au serveur.
    return render_template('arme/arme_delete.html', data = data_id_arme)


# ---------------------------------------------------------------------------------------------------
# OM 2019.04.02 Définition d'une "route" /armeUpdate , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# Permettre à l'utilisateur de modifier un arme, et de filtrer son entrée grâce à des expressions régulières REGEXP
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/arme_delete', methods=['POST', 'GET'])
def arme_delete():

    # OM 2019.04.02 Pour savoir si les données d'un formulaire sont un affichage ou un envoi de donnée par des champs utilisateurs.
    if request.method == 'POST':
        try:
            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_arme = Gestionarme()
            # OM 2019.04.02 Récupérer la valeur de "id_arme" du formulaire html "armeAfficher.html"
            id_arme_delete = request.form['id_arme_delete_html']
            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_delete_dictionnaire = {"value_id_arme": id_arme_delete}

            data_arme = obj_actions_arme.delete_arme_data(valeur_delete_dictionnaire)
            # OM 2019.04.02 On va afficher la liste des arme des concours
            # OM 2019.04.02 Envoie la page "HTML" au serveur. On passe un message d'information dans "message_html"

            # On affiche les arme
            return redirect(url_for('arme_afficher'))



        except (pymysql.err.OperationalError, pymysql.ProgrammingError, pymysql.InternalError, pymysql.IntegrityError,
                TypeError) as erreur:
            # OM 2020.04.09 Traiter spécifiquement l'erreur MySql 1451
            # Cette erreur 1451, signifie qu'on veut effacer un "arme" de concours qui est associé dans "t_arme_concours".
            if erreur.args[0] == 1451:
                # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                flash('IMPOSSIBLE d\'effacer !!! Cette valeur est associée à des concours !')
                # DEBUG bon marché : Pour afficher un message dans la console.
                print(f"IMPOSSIBLE d'effacer !! Ce arme est associé à des concours dans la t_arme_concours !!! : {erreur}")
                # Afficher la liste des arme des concours
                return redirect(url_for('arme_afficher'))
            else:
                # Communiquer qu'une autre erreur que la 1062 est survenue.
                # DEBUG bon marché : Pour afficher un message dans la console.
                print(f"Erreur arme_delete {erreur.args[0], erreur.args[1]}")
                # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                flash(f"Erreur arme_delete {erreur.args[0], erreur.args[1]}")


            # OM 2019.04.02 Envoie la page "HTML" au serveur.
    return render_template('arme/arme_afficher.html', data=data_arme)