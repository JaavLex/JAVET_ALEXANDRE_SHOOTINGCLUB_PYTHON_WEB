# erreurs.py
# OM 2020.04.09 Définition des erreurs "personnalisées"
# Quand il y a une erreur on doit définir des messages "clairs" à l'utilisateur
# Ne pas le laisser devant des erreurs incompréhensibles.
# Dérivation des classes standard des "except" dans les blocs "try...except"
import pymysql
from pymysql import IntegrityError


# OM 2020.04.12 Définition d'une classe qui permet, dès que "except" est détecté dans le bloc "try.. except MonErreur"
# @obj_mon_application.errorhandler(Exception) est activé et permet de transmettre le message "flash"
# à la "home.html". Voir le fichier "run_mon_app.py"
# c'est une dérivation des classes "standard built-in exceptions"
class MonErreur(Exception):
    pass


class MaBdErreurConnexion(Exception):
    pass


class MaBdErreurOperation(Exception):
    pass


class MaBdErreurDoublon(IntegrityError):
    pass


class MaBdErreurPyMySl(pymysql.Error):
    pass


class MaBdErreurDelete(pymysql.Error):
    pass


msg_erreurs = {
    "ErreurConnexionBD": {
        "message": "Pas de connexion à la BD ! Il faut démarrer un serveur MySql",
        "status": 400
    },
    "ErreurDoublonValue": {
        "message": "Cette valeur existe déjà.",
        "status": 400
    },
    "ErreurDictionnaire": {
        "message": "(OM du 104) Une valeur du dictionnaire n'existe pas !!!",
        "status": 400
    },
    "ErreurStructureTable": {
        "message": "Il y a un problème dans la structure des tables",
        "status": 400
    },
    "ErreurNomBD": {
        "message": "Problème avec le nom de la base de donnée",
        "status": 400
    },
    "ErreurPyMySql": {
        "message": "Problème en relation avec la BD",
        "status": 400
    },
    "ErreurDeleteContrainte": {
        "message": "Impossible d'effacer, car cette valeur est référencée ailleurs",
        "status": 400
    }
}



# OM 2020.04.16 En préparation pour galérer avec la gestion des erreurs
from pymysql.constants import ER

error_codes = {
    ER.TABLE_EXISTS_ERROR: "Table already exists",
    ER.ACCESS_DENIED_ERROR: "Access denied",
    ER.BAD_FIELD_ERROR: "Colonne inexistante"
}
