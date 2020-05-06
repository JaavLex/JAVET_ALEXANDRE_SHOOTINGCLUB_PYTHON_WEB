# run_mon_app.py
#
# OM 2020.03.29 Démonstration de l'utilisation du microframework Flask
# Des routes différentes sont définies
# Le retour des données se fait grâce à une page en HTML et le langage JINJA
# Avec le traitement de certaines erreurs.
# Ne pas abuser du try..except car il prend un peu plus de temps qu'un if (test classique)
# Une petite démo se trouve sur ce site :
# https://www.datacamp.com/community/tutorials/exception-handling-python

# Importation de la Class Flask
from flask import flash, render_template
from APP_SHOOTINGCLUB import obj_mon_application

# Pour définir sa propre page d'erreur 404
# Ce code est repris de la documentation FLASK
# https://flask-doc.readthedocs.io/en/latest/patterns/errorpages.html
@obj_mon_application.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# OM 2020.04.11 Grâce à la méthode "flash" cela permet de "raise" (remonter)
# les erreurs "try...execpt" dans la page "home.html"
@obj_mon_application.errorhandler(Exception)
def om_104_exception_handler(error):
    flash(error, "Danger")
    return render_template("home.html")


@obj_mon_application.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


@obj_mon_application.errorhandler(ConnectionRefusedError)
def conn_internal_error(error):
    return render_template('500.html'), 500


# OM 2020.04.09 Pour une démonstration "hors projet"
# Voir .... le fichier "routes.py" dans la fonction "personnes_taille_dict()"
# Dès qu'il y a un erreur "KeyError" dans le bloc try..except
# il vient "s'échouer"...ici
# il est possible de définir et de personnaliser chaque erreur comme on le désire
@obj_mon_application.errorhandler(KeyError)
def key_error(error):
    return render_template('keyerror.html'), 500


if __name__ == "__main__":
    # C'est bien le script principal "__main__" donc on l'interprète (démarre la démo d'utilisation de Flask).
    # Pour montrer qu'on peut paramétrer Flask :
    # On active le mode DEBUG
    # L'adresse IP du serveur mis en place par Flask peut être changée.
    # Pour ce fichier on impose le numéro du port.
    print("obj_mon_application.url_map ____> ", obj_mon_application.url_map)
    obj_mon_application.run(debug=True,
                            host="127.0.0.1",
                            port="1234")
