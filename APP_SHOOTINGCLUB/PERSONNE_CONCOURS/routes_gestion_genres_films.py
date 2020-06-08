# routes_gestion_concours_personne.py
# OM 2020.04.16 Gestions des "routes" FLASK pour la table intermédiaire qui associe les personne et les concours.

from flask import render_template, request, flash, session
from APP_SHOOTINGCLUB import obj_mon_application
from APP_SHOOTINGCLUB.CONCOURS.data_gestion_concours import GestionConcours
from APP_SHOOTINGCLUB.PERSONNE_CONCOURS.data_gestion_genres_films import Gestionconcourspersonne


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.26 Définition d'une "route" /concours_personne_afficher_concat
# Récupère la liste de tous les personne et de tous les concours associés aux personne.
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/concours_personne_afficher_concat/<int:id_personne_sel>", methods=['GET', 'POST'])
def concours_personne_afficher_concat (id_personne_sel):
    print("id_personne_sel ", id_personne_sel)
    if request.method == "GET":
        try:
            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_concours = Gestionconcourspersonne()
            # Récupère les données grâce à une requête MySql définie dans la classe Gestionconcours()
            # Fichier data_gestion_concours.py
            data_concours_personne_afficher_concat = obj_actions_concours.concours_personne_afficher_data_concat(id_personne_sel)
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print(" data concours", data_concours_personne_afficher_concat, "type ", type(data_concours_personne_afficher_concat))

            # Différencier les messages si la table est vide.
            if data_concours_personne_afficher_concat:
                # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données concours affichés dans concourspersonne!!", "success")
            else:
                flash(f"""Le personne demandé n'existe pas. Ou la table "t_concours_personne" est vide. !!""", "warning")
        except Exception as erreur:
            print(f"RGGF Erreur générale.")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # flash(f"RGG Exception {erreur}")
            raise Exception(f"RGGF Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # OM 2020.04.21 Envoie la page "HTML" au serveur.
    return render_template("personne_concours/concours_personne_afficher.html",
                           data=data_concours_personne_afficher_concat)


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.21 Définition d'une "route" /gf_edit_concours_personne_selected
# Récupère la liste de tous les concours du personne sélectionné.
# Nécessaire pour afficher tous les "TAGS" des concours, ainsi l'utilisateur voit les concours à disposition
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/gf_edit_concours_personne_selected", methods=['GET', 'POST'])
def gf_edit_concours_personne_selected ():
    if request.method == "GET":
        try:

            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_concours = GestionConcours()
            # Récupère les données grâce à une requête MySql définie dans la classe Gestionconcours()
            # Fichier data_gestion_concours.py
            # Pour savoir si la table "t_concours" est vide, ainsi on empêche l’affichage des tags
            # dans le render_template(concours_personne_modifier_tags_dropbox.html)
            data_concours_all = obj_actions_concours.concours_afficher_data('ASC', 0)

            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données de la table intermédiaire.
            obj_actions_concours = Gestionconcourspersonne()

            # OM 2020.04.21 Récupère la valeur de "id_personne" du formulaire html "concours_personne_afficher.html"
            # l'utilisateur clique sur le lien "Modifier concours de ce personne" et on récupère la valeur de "id_personne" grâce à la variable "id_personne_concours_edit_html"
            # <a href="{{ url_for('gf_edit_concours_personne_selected', id_personne_concours_edit_html=row.id_personne) }}">Modifier les concours de ce personne</a>
            id_personne_concours_edit = request.values['id_personne_concours_edit_html']

            # OM 2020.04.21 Mémorise l'id du personne dans une variable de session
            # (ici la sécurité de l'application n'est pas engagée)
            # il faut éviter de stocker des données sensibles dans des variables de sessions.
            session['session_id_personne_concours_edit'] = id_personne_concours_edit

            # Constitution d'un dictionnaire pour associer l'id du personne sélectionné avec un nom de variable
            valeur_id_personne_selected_dictionnaire = {"value_id_personne_selected": id_personne_concours_edit}

            # Récupère les données grâce à 3 requêtes MySql définie dans la classe Gestionconcourspersonne()
            # 1) Sélection du personne choisi
            # 2) Sélection des concours "déjà" attribués pour le personne.
            # 3) Sélection des concours "pas encore" attribués pour le personne choisi.
            # Fichier data_gestion_concours_personne.py
            # ATTENTION à l'ordre d'assignation des variables retournées par la fonction "concours_personne_afficher_data"
            data_concours_personne_selected, data_concours_personne_non_attribues, data_concours_personne_attribues = \
                obj_actions_concours.concours_personne_afficher_data(valeur_id_personne_selected_dictionnaire)

            lst_data_personne_selected = [item['id_personne'] for item in data_concours_personne_selected]
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print("lst_data_personne_selected  ", lst_data_personne_selected,
                  type(lst_data_personne_selected))

            # Dans le composant "tags-selector-tagselect" on doit connaître
            # les concours qui ne sont pas encore sélectionnés.
            lst_data_concours_personne_non_attribues = [item['id_concours'] for item in data_concours_personne_non_attribues]
            session['session_lst_data_concours_personne_non_attribues'] = lst_data_concours_personne_non_attribues
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print("lst_data_concours_personne_non_attribues  ", lst_data_concours_personne_non_attribues,
                  type(lst_data_concours_personne_non_attribues))

            # Dans le composant "tags-selector-tagselect" on doit connaître
            # les concours qui sont déjà sélectionnés.
            lst_data_concours_personne_old_attribues = [item['id_concours'] for item in data_concours_personne_attribues]
            session['session_lst_data_concours_personne_old_attribues'] = lst_data_concours_personne_old_attribues
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print("lst_data_concours_personne_old_attribues  ", lst_data_concours_personne_old_attribues,
                  type(lst_data_concours_personne_old_attribues))

            # DEBUG bon marché : Pour afficher le résultat et son type.
            print(" data data_concours_personne_selected", data_concours_personne_selected, "type ", type(data_concours_personne_selected))
            print(" data data_concours_personne_non_attribues ", data_concours_personne_non_attribues, "type ",
                  type(data_concours_personne_non_attribues))
            print(" data_concours_personne_attribues ", data_concours_personne_attribues, "type ",
                  type(data_concours_personne_attribues))

            # Extrait les valeurs contenues dans la table "t_concours", colonne "date_concours"
            # Le composant javascript "tagify" pour afficher les tags n'a pas besoin de l'id_concours
            lst_data_concours_personne_non_attribues = [item['date_concours'] for item in data_concours_personne_non_attribues]
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print("lst_all_concours gf_edit_concours_personne_selected ", lst_data_concours_personne_non_attribues,
                  type(lst_data_concours_personne_non_attribues))

            # Différencier les messages si la table est vide.
            if lst_data_personne_selected == [None]:
                flash(f"""Le personne demandé n'existe pas. Ou la table "t_concours_personne" est vide. !!""", "warning")
            else:
                # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données concours affichées dans concourspersonne!!", "success")

        except Exception as erreur:
            print(f"RGGF Erreur générale.")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)"
            # fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # flash(f"RGG Exception {erreur}")
            raise Exception(f"RGGF Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # OM 2020.04.21 Envoie la page "HTML" au serveur.
    return render_template("personne_concours/concours_personne_modifier_tags_dropbox.html",
                           data_concours=data_concours_all,
                           data_personne_selected=data_concours_personne_selected,
                           data_concours_attribues=data_concours_personne_attribues,
                           data_concours_non_attribues=data_concours_personne_non_attribues)


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.26 Définition d'une "route" /gf_update_concours_personne_selected
# Récupère la liste de tous les concours du personne sélectionné.
# Nécessaire pour afficher tous les "TAGS" des concours, ainsi l'utilisateur voit les concours à disposition
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/gf_update_concours_personne_selected", methods=['GET', 'POST'])
def gf_update_concours_personne_selected ():
    if request.method == "POST":
        try:
            # Récupère l'id du personne sélectionné
            id_personne_selected = session['session_id_personne_concours_edit']
            print("session['session_id_personne_concours_edit'] ", session['session_id_personne_concours_edit'])

            # Récupère la liste des concours qui ne sont pas associés au personne sélectionné.
            old_lst_data_concours_personne_non_attribues = session['session_lst_data_concours_personne_non_attribues']
            print("old_lst_data_concours_personne_non_attribues ", old_lst_data_concours_personne_non_attribues)

            # Récupère la liste des concours qui sont associés au personne sélectionné.
            old_lst_data_concours_personne_attribues = session['session_lst_data_concours_personne_old_attribues']
            print("old_lst_data_concours_personne_old_attribues ", old_lst_data_concours_personne_attribues)

            # Effacer toutes les variables de session.
            session.clear()

            # Récupère ce que l'utilisateur veut modifier comme concours dans le composant "tags-selector-tagselect"
            # dans le fichier "concours_personne_modifier_tags_dropbox.html"
            new_lst_str_concours_personne = request.form.getlist('name_select_tags')
            print("new_lst_str_concours_personne ", new_lst_str_concours_personne)

            # OM 2020.04.29 Dans "name_select_tags" il y a ['4','65','2']
            # On transforme en une liste de valeurs numériques. [4,65,2]
            new_lst_int_concours_personne_old = list(map(int, new_lst_str_concours_personne))
            print("new_lst_concours_personne ", new_lst_int_concours_personne_old, "type new_lst_concours_personne ",
                  type(new_lst_int_concours_personne_old))

            # Pour apprécier la facilité de la vie en Python... "les ensembles en Python"
            # https://fr.wikibooks.org/wiki/Programmation_Python/Ensembles
            # OM 2020.04.29 Une liste de "id_concours" qui doivent être effacés de la table intermédiaire "t_concours_personne".
            lst_diff_concours_delete_b = list(
                set(old_lst_data_concours_personne_attribues) - set(new_lst_int_concours_personne_old))
            # DEBUG bon marché : Pour afficher le résultat de la liste.
            print("lst_diff_concours_delete_b ", lst_diff_concours_delete_b)

            # OM 2020.04.29 Une liste de "id_concours" qui doivent être ajoutés à la BD
            lst_diff_concours_insert_a = list(
                set(new_lst_int_concours_personne_old) - set(old_lst_data_concours_personne_attribues))
            # DEBUG bon marché : Pour afficher le résultat de la liste.
            print("lst_diff_concours_insert_a ", lst_diff_concours_insert_a)

            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_concours = Gestionconcourspersonne()

            # Pour le personne sélectionné, parcourir la liste des concours à INSÉRER dans la "t_concours_personne".
            # Si la liste est vide, la boucle n'est pas parcourue.
            for id_concours_ins in lst_diff_concours_insert_a:
                # Constitution d'un dictionnaire pour associer l'id du personne sélectionné avec un nom de variable
                # et "id_concours_ins" (l'id du concours dans la liste) associé à une variable.
                valeurs_personne_sel_concours_sel_dictionnaire = {"value_fk_personne": id_personne_selected,
                                                           "value_fk_concours": id_concours_ins}
                # Insérer une association entre un(des) concours(s) et le personne sélectionner.
                obj_actions_concours.concours_personne_add(valeurs_personne_sel_concours_sel_dictionnaire)

            # Pour le personne sélectionné, parcourir la liste des concours à EFFACER dans la "t_concours_personne".
            # Si la liste est vide, la boucle n'est pas parcourue.
            for id_concours_del in lst_diff_concours_delete_b:
                # Constitution d'un dictionnaire pour associer l'id du personne sélectionné avec un nom de variable
                # et "id_concours_del" (l'id du concours dans la liste) associé à une variable.
                valeurs_personne_sel_concours_sel_dictionnaire = {"value_fk_personne": id_personne_selected,
                                                           "value_fk_concours": id_concours_del}
                # Effacer une association entre un(des) concours(s) et le personne sélectionner.
                obj_actions_concours.concours_personne_delete(valeurs_personne_sel_concours_sel_dictionnaire)

            # Récupère les données grâce à une requête MySql définie dans la classe Gestionconcours()
            # Fichier data_gestion_concours.py
            # Afficher seulement le personne dont les concours sont modifiés, ainsi l'utilisateur voit directement
            # les changements qu'il a demandés.
            data_concours_personne_afficher_concat = obj_actions_concours.concours_personne_afficher_data_concat(id_personne_selected)
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print(" data concours", data_concours_personne_afficher_concat, "type ", type(data_concours_personne_afficher_concat))

            # Différencier les messages si la table est vide.
            if data_concours_personne_afficher_concat == None:
                flash(f"""Le personne demandé n'existe pas. Ou la table "t_concours_personne" est vide. !!""", "warning")
            else:
                # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données concours affichées dans concourspersonne!!", "success")

        except Exception as erreur:
            print(f"RGGF Erreur générale.")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # flash(f"RGG Exception {erreur}")
            raise Exception(f"RGGF Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # Après cette mise à jour de la table intermédiaire "t_concours_personne",
    # on affiche les personne et le(urs) concours(s) associé(s).
    return render_template("personne_concours/concours_personne_afficher.html",
                           data=data_concours_personne_afficher_concat)
