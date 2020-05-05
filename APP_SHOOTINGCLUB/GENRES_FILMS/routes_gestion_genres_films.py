# routes_gestion_genres_films.py
# OM 2020.04.16 Gestions des "routes" FLASK pour la table intermédiaire qui associe les films et les genres.
from flask import render_template
from APP_SHOOTINGCLUB import obj_mon_application


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.07 Définition d'une "route" /genres_films_afficher
# cela va permettre de programmer les actions avant d'interagir
# avec le navigateur par la méthode "render_template"
# Pour tester http://127.0.0.1:1234/genres_films_afficher
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/genres_films_afficher", methods=['GET', 'POST'])
def genres_films_afficher():
    # # OM 2020.04.09 Pour savoir si les données d'un formulaire sont un affichage
    # # ou un envoi de donnée par des champs du formulaire HTML.
    # if request.method == "GET":
    #     try:
    #         # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
    #         obj_actions_genres_films = GestionFilmsGenres()
    #         # Récupére les données grâce à une requête MySql définie dans la classe GestionGenres()
    #         # Fichier data_gestion_genres.py
    #         data_genres_films = obj_actions_genres_films.genres_afficher_data()
    #         # DEBUG bon marché : Pour afficher un message dans la console.
    #
    #         # OM 2020.04.09 La ligns ci-après permet de donner un sentiment rassurant aux utilisateurs.
    #         flash("Données genres de films affichées !!", "Success")
    #     except Exception as erreur:
    #         print(f"RGFG Erreur générale.")
    #         # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
    #         # Ainsi on peut avoir un message d'erreur personnalisé.
    #         # flash(f"RGG Exception {erreur}")
    #         raise Exception(f"RGFG Erreur générale. {erreur}")

    # OM 2020.04.07 Envoie la page "HTML" au serveur.
    return render_template("genres_films/genres_films_afficher.html")

