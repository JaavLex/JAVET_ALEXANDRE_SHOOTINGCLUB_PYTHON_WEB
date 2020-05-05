# routes.py
# OM 2020.04.02 Pour faire des tests divers et variés.

from flask import render_template
from APP_SHOOTINGCLUB import obj_mon_application
from APP_SHOOTINGCLUB.DATABASE.erreurs import *


@obj_mon_application.route('/index')
def index():
    return "Hello, World!"


@obj_mon_application.route('/')
@obj_mon_application.route('/essai')
def home_dans_routes_pour_exemple_hommage_m_el_vyn_mal_herbe():
    return render_template("home.html")

# OM 2020.04.09 Pour une démonstration du traitement d'erreurs avec "raise"
# Pour tester cette fonction: http://127.0.0.1:1234/taillepersonne
@obj_mon_application.route('/taillepersonne')
def personnes_taille_dict():
    # DEBUG bon marché : Pour afficher dans la console les valeurs des erreurs "customisées"
    # dans le fichier "DATABASE/erreurs.py" et le type de ces valeurs.
    print("msg_erreurs ", msg_erreurs, "type msg_erreurs ",type(msg_erreurs))

    # Affiche les valeurs et les clés
    print(msg_erreurs.items())
    # Affiche les clés
    print(msg_erreurs.keys())
    # Afficher les valeurs
    print(msg_erreurs.values())

    # Affiche la valeur "message" du dictionnaires d'erreur "DATABASE/erreurs.py"
    print("val dans le dict ", msg_erreurs['ErreurDictionnaire'])

    # Défini un petit dictionnaire
    taille_personnes_dict = {"OM" : 194, "Gégé" : 175, "Hugo" : 163}
    #
    # OM 2020.04.09 Pour vos essais, il suffit d'enlever le # pour voir comment fonctionne pratiquement
    # le traitement de l'erreur.
    # Si la chaîne de caractère ne se trouve pas dans le dictionnaire ci-dessus il va y avoir une erreur "KeyError"
    # On la capture et on renvoie un texte "personnel" (custom error handler) à l'utilisateur.
    nom_personne = "OM"
    # nom_personne = "Gégé"
    # nom_personne = "Hugo"

    # nom_personne = "Pignon"

    try:
        # Tout se passe normalement
        print(f'{nom_personne} mesure {taille_personnes_dict[nom_personne]} [cm]')
    except KeyError as erreur:
        # Une personne ne se trouve pas dans le dictionnaire
        # DEBUG bon marché : Pour afficher un message d'erreur dans la console
        print(f"{nom_personne} n'existe pas !")

        # Pour vos essais... constater les différentes actions avec "raise"
        # pour les 2 ci-dessous, il renvoie une page "keyerror.html"
        # grâce à "@obj_mon_application.errorhandler(KeyError)" défini dans le fichier "run_mon_app.py"
        # raise KeyError
        # raise erreur

        # Il renvoie simplement la valeur du contenu de "erreur"
        # grâce à la classe "MonErreur(Exception)" dans le fichier "erreurs.py"
        # raise MonErreur(erreur)

        # Il renvoie un texte avec la valeur de "nom_personne" et c'est dans le fichier
        # grâce à la classe "MonErreur(Exception)" dans le fichier "erreurs.py"
        # raise MonErreur(f"il y a une erreur ! La personne {nom_personne} n'existe pas dans le dictionnaire")

        # Celle-ci est assez complète... mais il y a toujours mieux
        # Il renvoie un texte avec la valeur de "nom_personne" ainsi qu'un message personnalisé
        # grâce à la classe "MonErreur(Exception)" dans le fichier "erreurs.py"
        raise MonErreur(f"{msg_erreurs['ErreurDictionnaire']['message']} "
                        f"Le nom : {nom_personne} n'est pas une valeur contenue dans le dictionnaire")

    return render_template("zzz_essais_om_104/exception_raise_custom_om_104.html")
