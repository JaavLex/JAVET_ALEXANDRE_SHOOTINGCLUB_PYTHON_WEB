# routes_gestion_stand_de_tir.py
# OM 2020.04.06 Gestions des "routes" FLASK pour les stand_de_tir.

from flask import render_template, flash, redirect, url_for, request
from APP_SHOOTINGCLUB import obj_mon_application
from APP_SHOOTINGCLUB.STAND_DE_TIR.data_gestion_stand_de_tir import Gestionstand_de_tir
from APP_SHOOTINGCLUB.DATABASE.erreurs import *
# OM 2020.04.10 Pour utiliser les expressions régulières REGEX
import re


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.07 Définition d'une "route" /stand_de_tir_afficher
# cela va permettre de programmer les actions avant d'interagir
# avec le navigateur par la méthode "render_template"
# Pour tester http://127.0.0.1:1234/stand_de_tir<td>{{ row.nom_pers }}</td>_afficher
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/stand_de_tir_afficher", methods=['GET', 'POST'])
def stand_de_tir_afficher():
    # OM 2020.04.09 Pour savoir si les données d'un formulaire sont un affichage
    # ou un envoi de donnée par des champs du formulaire HTML.
    if request.method == "GET":
        try:
            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_stand_de_tir = Gestionstand_de_tir()
            # Récupére les données grâce à une requête MySql définie dans la classe Gestionstand_de_tir()
            # Fichier data_gestion_stand_de_tir.py
            data_stand_de_tir = obj_actions_stand_de_tir.stand_de_tir_afficher_data()
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(" data stand_de_tir", data_stand_de_tir, "type ", type(data_stand_de_tir))

            # OM 2020.04.09 La ligns ci-après permet de donner un sentiment rassurant aux utilisateurs.
            flash("Données stand_de_tir affichées !!", "Success")
        except Exception as estand_de_tirsrreur:
            print(f"RGG Erreur générale.")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # flash(f"RGG Exception {erreur}")
            raise Exception(f"RGG Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # OM 2020.04.07 Envoie la page "HTML" au serveur.
    return render_template("stand_de_tir/stand_de_tir_afficher.html", data=data_stand_de_tir)


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.07 Définition d'une "route" /stand_de_tir_add ,
# cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template"
# En cas d'erreur on affiche à nouveau la page "stand_de_tir_add.html"
# Pour la tester http://127.0.0.1:1234/stand_de_tir_add
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/stand_de_tir_add", methods=['GET', 'POST'])
def stand_de_tir_add():
    # OM 2019.03.25 Pour savoir si les données d'un formulaire sont un affichage
    # ou un envoi de donnée par des champs utilisateurs.
    if request.method == "POST":
        try:
            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_stand_de_tir = Gestionstand_de_tir()
            # OM 2020.04.09 Récupère le contenu du champ dans le formulaire HTML "stand_de_tir_add.html"
            nom_stand_de_tir = request.form['nom_stand_de_tir_html']
            adresse_stand_de_tir = request.form['adresse_stand_de_tir_html']
            tel_stand_de_tir = request.form['tel_stand_de_tir_html']

            # OM 2019.04.04 On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
            # des valeurs avec des caractères qui ne sont pas des lettres.
            # Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
            if not re.match("",
                                nom_stand_de_tir):
                # OM 2019.03.28 Message humiliant à l'attention de l'utilisateur.
                flash(f"Une entrée...incorrecte !! Pas de chiffres, de caractères spéciaux, d'espace à double, "
                      f"de double apostrophe, de double trait union et ne doit pas être vide.", "Danger")
                # On doit afficher à nouveau le formulaire "stand_de_tir_add.html" à cause des erreurs de "claviotage"
                return render_template("stand_de_tir/stand_de_tir_add.html")
            else:

                # Constitution d'un dictionnaire et insertion dans la BD
                valeurs_insertion_dictionnaire = {"value_nom_stand_de_tir": nom_stand_de_tir, "value_adresse_stand_de_tir": adresse_stand_de_tir, "value_tel_stand_de_tir": tel_stand_de_tir}
                obj_actions_stand_de_tir.add_stand_de_tir_data(valeurs_insertion_dictionnaire)

                # OM 2019.03.25 Les 2 lignes ci-après permettent de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données insérées !!", "Sucess")
                print(f"Données insérées !!")
                # On va interpréter la "route" 'stand_de_tir_afficher', car l'utilisateur
                # doit voir le nouveau stand_de_tir qu'il vient d'insérer.
                return redirect(url_for('stand_de_tir_afficher'))

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
    return render_template("stand_de_tir/stand_de_tir_add.html")


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.07 Définition d'une "route" /stand_de_tir_edit , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# On change la valeur d'un stand_de_tir de concours par la commande MySql "UPDATE"
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/stand_de_tir_edit', methods=['POST', 'GET'])
def stand_de_tir_edit():
    # OM 2020.04.07 Les données sont affichées dans un formulaire, l'affichage de la sélection
    # d'une seule ligne choisie par le bouton "edit" dans le formulaire "stand_de_tir_afficher.html"
    if request.method == 'GET':
        try:
            # Récupérer la valeur de "id_stand_de_tir" du formulaire html "stand_de_tir_afficher.html"
            # l'utilisateur clique sur le lien "edit" et on récupére la valeur de "id_stand_de_tir"
            # grâce à la variable "id_stand_de_tir_edit_html"
            # <a href="{{ url_for('stand_de_tir_edit', id_stand_de_tir_edit_html=row.id_stand_de_tir) }}">Edit</a>
            id_stand_de_tir_edit = request.values['id_stand_de_tir_edit_html']

            # Pour afficher dans la console la valeur de "id_stand_de_tir_edit", une façon simple de se rassurer,
            # sans utiliser le DEBUGGER
            print(id_stand_de_tir_edit)

            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_select_dictionnaire = {"value_id_stand_de_tir": id_stand_de_tir_edit}

            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_stand_de_tir = Gestionstand_de_tir()

            # OM 2019.04.02 La commande MySql est envoyée à la BD
            data_id_stand_de_tir = obj_actions_stand_de_tir.edit_stand_de_tir_data(valeur_select_dictionnaire)
            print("dataIdstand_de_tir ", data_id_stand_de_tir, "type ", type(data_id_stand_de_tir))
            # Message ci-après permettent de donner un sentiment rassurant aux utilisateurs.
            flash(f"Editer le stand_de_tir d'un per !!!")

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

    return render_template("stand_de_tir/stand_de_tir_edit.html", data=data_id_stand_de_tir)


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.07 Définition d'une "route" /stand_de_tir_update , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# On change la valeur d'un stand_de_tir de concours par la commande MySql "UPDATE"
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/stand_de_tir_update', methods=['POST', 'GET'])
def stand_de_tir_update():
    # DEBUG bon marché : Pour afficher les méthodes et autres de la classe "flask.request"
    print(dir(request))
    # OM 2020.04.07 Les données sont affichées dans un formulaire, l'affichage de la sélection
    # d'une seule ligne choisie par le bouton "edit" dans le formulaire "stand_de_tir_afficher.html"
    # Une fois que l'utilisateur à modifié la valeur du stand_de_tir alors il va appuyer sur le bouton "UPDATE"
    # donc en "POST"
    if request.method == 'POST':
        try:
            # DEBUG bon marché : Pour afficher les valeurs contenues dans le formulaire
            print("request.values ",request.values)

            # Récupérer la valeur de "id_stand_de_tir" du formulaire html "stand_de_tir_edit.html"
            # l'utilisateur clique sur le lien "edit" et on récupére la valeur de "id_stand_de_tir"
            # grâce à la variable "id_stand_de_tir_edit_html"
            # <a href="{{ url_for('stand_de_tir_edit', id_stand_de_tir_edit_html=row.id_stand_de_tir) }}">Edit</a>
            id_stand_de_tir_edit = request.values['id_stand_de_tir_edit_html']
            nom_stand_de_tir_edit = request.values['nom_stand_de_tir_html']
            adresse_stand_de_tir_edit = request.values['adresse_stand_de_tir_html']
            tel_stand_de_tir_edit = request.values['tel_stand_de_tir_html']

            # Récupère le contenu du champ "intitule_stand_de_tir" dans le formulaire HTML "stand_de_tirEdit.html"

            valeur_edit_list = [{'id_stand_de_tir': id_stand_de_tir_edit, 'nom_stand_de_tir': nom_stand_de_tir_edit, 'adresse_stand_de_tir': adresse_stand_de_tir_edit, 'tel_stand_de_tir': tel_stand_de_tir_edit}]
            # On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
            # des valeurs avec des caractères qui ne sont pas des lettres.
            # Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
            if not re.match("", nom_stand_de_tir_edit):
                # En cas d'erreur, conserve la saisie fausse, afin que l'utilisateur constate sa misérable faute
                # Récupère le contenu du champ "intitule_stand_de_tir" dans le formulaire HTML "stand_de_tirEdit.html"
                #nom_pers = request.values['name_edit_intitule_stand_de_tir_html']
                # Message humiliant à l'attention de l'utilisateur.
                flash(f"Une entrée...incorrecte !! Pas de chiffres, de caractères spéciaux, d'espace à double, "
                      f"de double apostrophe, de double trait union et ne doit pas être vide.", "Danger")

                # On doit afficher à nouveau le formulaire "stand_de_tir_edit.html" à cause des erreurs de "claviotage"
                # Constitution d'une liste pour que le formulaire d'édition "stand_de_tir_edit.html" affiche à nouveau
                # la possibilité de modifier l'entrée
                # Exemple d'une liste : [{'id_stand_de_tir': 13, 'intitule_stand_de_tir': 'philosophique'}]
                valeur_edit_list = [{'id_stand_de_tir': id_stand_de_tir_edit, 'nom_stand_de_tir': nom_stand_de_tir_edit, 'adresse_stand_de_tir': adresse_stand_de_tir_edit, 'tel_stand_de_tir': tel_stand_de_tir_edit}]

                # DEBUG bon marché :
                # Pour afficher le contenu et le type de valeurs passées au formulaire "stand_de_tir_edit.html"
                print(valeur_edit_list, "type ..",  type(valeur_edit_list))
                return render_template('stand_de_tir/stand_de_tir_edit.html', data=valeur_edit_list)
            else:
                # Constitution d'un dictionnaire et insertion dans la BD
                valeur_update_dictionnaire = {"value_id_stand_de_tir": id_stand_de_tir_edit, "value_nom_stand_de_tir": nom_stand_de_tir_edit, "value_adresse_stand_de_tir": adresse_stand_de_tir_edit, 'value_tel_stand_de_tir': tel_stand_de_tir_edit}

                # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
                obj_actions_stand_de_tir = Gestionstand_de_tir()

                # La commande MySql est envoyée à la BD
                data_id_stand_de_tir = obj_actions_stand_de_tir.update_stand_de_tir_data(valeur_update_dictionnaire)
                # DEBUG bon marché :
                print("dataIdstand_de_tir ", data_id_stand_de_tir, "type ", type(data_id_stand_de_tir))
                # Message ci-après permettent de donner un sentiment rassurant aux utilisateurs.
                flash(f"Editer le stand_de_tir d'un per !!!")
                # On affiche les stand_de_tir
                return redirect(url_for('stand_de_tir_afficher'))

        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:

            print(erreur.args)
            flash(f"problème stand_de_tir update{erreur.args[0]}")
            # En cas de problème, mais surtout en cas de non respect
            # des régles "REGEX" dans le champ "name_edit_intitule_stand_de_tir_html" alors on renvoie le formulaire "EDIT"
            return render_template('stand_de_tir/stand_de_tir_edit.html', data=valeur_edit_list)

    return render_template("stand_de_tir/stand_de_tir_update.html")


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.07 Définition d'une "route" /stand_de_tir_select_delete , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# On change la valeur d'un stand_de_tir de concours par la commande MySql "UPDATE"
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/stand_de_tir_select_delete', methods=['POST', 'GET'])
def stand_de_tir_select_delete():

    if request.method == 'GET':
        try:

            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_stand_de_tir = Gestionstand_de_tir()
            # OM 2019.04.04 Récupérer la valeur de "idstand_de_tirDeleteHTML" du formulaire html "stand_de_tirDelete.html"
            id_stand_de_tir_delete = request.args.get('id_stand_de_tir_delete_html')

            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_delete_dictionnaire = {"value_id_stand_de_tir": id_stand_de_tir_delete}


            # OM 2019.04.02 La commande MySql est envoyée à la BD
            data_id_stand_de_tir = obj_actions_stand_de_tir.delete_select_stand_de_tir_data(valeur_delete_dictionnaire)
            flash(f"EFFACER et c'est terminé pour cette \"POV\" valeur !!!")

        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:
            # Communiquer qu'une erreur est survenue.
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Erreur stand_de_tir_delete {erreur.args[0], erreur.args[1]}")
            # C'est une erreur à signaler à l'utilisateur de cette application WEB.
            flash(f"Erreur stand_de_tir_delete {erreur.args[0], erreur.args[1]}")

    # Envoie la page "HTML" au serveur.
    return render_template('stand_de_tir/stand_de_tir_delete.html', data = data_id_stand_de_tir)


# ---------------------------------------------------------------------------------------------------
# OM 2019.04.02 Définition d'une "route" /stand_de_tirUpdate , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# Permettre à l'utilisateur de modifier un stand_de_tir, et de filtrer son entrée grâce à des expressions régulières REGEXP
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/stand_de_tir_delete', methods=['POST', 'GET'])
def stand_de_tir_delete():

    # OM 2019.04.02 Pour savoir si les données d'un formulaire sont un affichage ou un envoi de donnée par des champs utilisateurs.
    if request.method == 'POST':
        try:
            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_stand_de_tir = Gestionstand_de_tir()
            # OM 2019.04.02 Récupérer la valeur de "id_stand_de_tir" du formulaire html "stand_de_tirAfficher.html"
            id_stand_de_tir_delete = request.form['id_stand_de_tir_delete_html']
            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_delete_dictionnaire = {"value_id_stand_de_tir": id_stand_de_tir_delete}

            data_stand_de_tir = obj_actions_stand_de_tir.delete_stand_de_tir_data(valeur_delete_dictionnaire)
            # OM 2019.04.02 On va afficher la liste des stand_de_tir des concours
            # OM 2019.04.02 Envoie la page "HTML" au serveur. On passe un message d'information dans "message_html"

            # On affiche les stand_de_tir
            return redirect(url_for('stand_de_tir_afficher'))



        except (pymysql.err.OperationalError, pymysql.ProgrammingError, pymysql.InternalError, pymysql.IntegrityError,
                TypeError) as erreur:
            # OM 2020.04.09 Traiter spécifiquement l'erreur MySql 1451
            # Cette erreur 1451, signifie qu'on veut effacer un "stand_de_tir" de concours qui est associé dans "t_stand_de_tir_concours".
            if erreur.args[0] == 1451:
                # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                flash('IMPOSSIBLE d\'effacer !!! Cette valeur est associée à des concours !')
                # DEBUG bon marché : Pour afficher un message dans la console.
                print(f"IMPOSSIBLE d'effacer !! Ce stand_de_tir est associé à des concours dans la t_stand_de_tir_concours !!! : {erreur}")
                # Afficher la liste des stand_de_tir des concours
                return redirect(url_for('stand_de_tir_afficher'))
            else:
                # Communiquer qu'une autre erreur que la 1062 est survenue.
                # DEBUG bon marché : Pour afficher un message dans la console.
                print(f"Erreur stand_de_tir_delete {erreur.args[0], erreur.args[1]}")
                # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                flash(f"Erreur stand_de_tir_delete {erreur.args[0], erreur.args[1]}")


            # OM 2019.04.02 Envoie la page "HTML" au serveur.
    return render_template('stand_de_tir/stand_de_tir_afficher.html', data=data_stand_de_tir)