-- Auteur :         Javet Alexandre
-- Dernier edit :   11-03-2020 9:09PM
-- Sujet database : Shooting Club
-- Module :         104

-- PERSONNES --
-- Afficher toutes les personnes
SELECT * FROM T_Personne
-- (OPTIONNEL) OUTILS DE RECHERCHE POUR AFFINER --
-- OPTION 1 --
WHERE T1.id_personne = -- INSERER ID ICI --
-- OPTION 2 --
WHERE T1.nom_pers = -- INSERER NOM DE FAMILLE ICI --
---

-- Afficher les informations importantes
SELECT nom_pers, prenom_pers, date_de_naissance, possession_arme FROM T_Personne
-- (OPTIONNEL) OUTILS DE RECHERCHE POUR AFFINER --
-- OPTION 1 --
WHERE T1.id_personne = -- INSERER ID ICI --
-- OPTION 2 --
WHERE T1.nom_pers = -- INSERER NOM DE FAMILLE ICI --
---

-- Afficher les scores par personnes par concours + infos pratiques
SELECT id_personne_a_score, nom_pers, prenom_pers, date_de_naissance, possession_arme, id_concours, date_concours, type_concours, nom_stand_de_tir, adresse_stand_de_tir, score_cible1, score_cible2, score_cible3, score_cible4, score_total FROM T_Personne AS T1
INNER JOIN T_Personne_a_scores AS T2 On T2.fk_personne = T1.id_personne
INNER JOIN T_Scores AS T3 ON T3.id_scores = T2.fk_scores
INNER JOIN T_Concours AS T4 ON T4.id_concours = T2.fk_concours
INNER JOIN T_Type_concours AS T5 ON T5.id_type_concours = T4.fk_type_concours
INNER JOIN T_Stand_de_tir AS T6 ON T6.id_stand_de_tir = T4.fk_stand_de_tir
-- (OPTIONNEL) OUTILS DE RECHERCHE POUR AFFINER --
-- OPTION 1 --
WHERE T1.id_personne = -- INSERER ID ICI --
-- OPTION 2 --
WHERE T1.nom_pers = -- INSERER NOM DE FAMILLE ICI --
---

-- CONCOURS --
-- Affiche les présences dans les concours + informations pratiques
SELECT id_concours, date_concours, type_concours, nom_stand_de_tir, adresse_stand_de_tir, nom_pers, prenom_pers, possession_arme FROM T_Concours AS T1
INNER JOIN T_Type_concours AS FK1 ON T1.fk_type_concours = FK1.id_type_concours
INNER JOIN T_Stand_de_tir AS FK2 ON T1.fk_stand_de_tir = FK2.id_stand_de_tir
INNER JOIN T_Concours_a_presence AS T2 ON T1.id_concours = T2.fk_concours
INNER JOIN T_Personne AS T3 ON T2.fk_personne = T3.id_personne
-- (OPTIONNEL) OUTILS DE RECHERCHE POUR AFFINER --
-- OPTION 1 --
WHERE T1.id_concours = -- INSERER ID ICI --
-- OPTION 2 --
WHERE T1.date_concours = -- INSERER DATE DU CONCOURS --
-- OPTION 3 --
WHERE FK1.type_concours = -- INSERER TYPE DE CONCOURS --
---

-- Affiche les locations des armes durant les concours + infos supplémentaires sur l'arme en question
SELECT id_concours, date_concours, type_concours, nom_stand_de_tir, adresse_stand_de_tir, nom_arme, type_arme, calibre, prix_location  FROM T_Concours AS T1
INNER JOIN T_Type_concours AS FK1 ON T1.fk_type_concours = FK1.id_type_concours
INNER JOIN T_Stand_de_tir AS FK2 ON T1.fk_stand_de_tir = FK2.id_stand_de_tir
INNER JOIN T_Concours_location_arme AS T2 ON T2.fk_concours = T1.id_concours
INNER JOIN T_Armes AS T3 ON T2.fk_arme = T3.id_arme
INNER JOIN T_Type_arme AS T4 ON T3.fk_type_arme = T4.id_type_arme
INNER JOIN T_Munition AS T5 ON T3.fk_munition = T5.id_munition
-- (OPTIONNEL) OUTILS DE RECHERCHE POUR AFFINER --
-- OPTION 1 --
WHERE T1.id_concours = -- INSERER ID ICI --
-- OPTION 2 --
WHERE T1.date_concours = -- INSERER DATE DU CONCOURS --
-- OPTION 3 --
WHERE FK1.type_concours = -- INSERER TYPE DE CONCOURS --
---

-- Affiche la consommation de munitions par personne par concours + calibre + prix pour 50 cartouches de ce calibre
SELECT id_concours, date_concours, type_concours, nom_stand_de_tir, adresse_stand_de_tir, nom_pers, prenom_pers, calibre, prix_p_50, nb_munitions FROM T_Concours AS T1
INNER JOIN T_Type_concours AS FK1 ON T1.fk_type_concours = FK1.id_type_concours
INNER JOIN T_Stand_de_tir AS FK2 ON T1.fk_stand_de_tir = FK2.id_stand_de_tir
INNER JOIN T_Concours_a_munitions_tirees AS T2 ON T2.fk_concours = T1.id_concours
INNER JOIN T_Munition AS T3 ON T3.id_munition = T2.fk_munition
INNER JOIN T_Personne AS T4 ON T4.id_personne = T2.fk_personne
-- (OPTIONNEL) OUTILS DE RECHERCHE POUR AFFINER --
-- OPTION 1 --
WHERE T1.id_concours = -- INSERER ID ICI --
-- OPTION 2 --
WHERE T1.date_concours = -- INSERER DATE DU CONCOURS --
-- OPTION 3 --
WHERE FK1.type_concours = -- INSERER TYPE DE CONCOURS --
---
