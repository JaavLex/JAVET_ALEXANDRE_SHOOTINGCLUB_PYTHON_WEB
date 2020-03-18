# insert_table_values.py
# Javet Alexandre - 18.03.2020 20:28
import Javet_Alexandre_2020_1D_connectdb
from INSERT import Javet_Alexandre_2020_1D_insertintotable


try:
    connection = Javet_Alexandre_2020_1D_connectdb.DatabaseTools()

    insert_records = Javet_Alexandre_2020_1D_insertintotable.DbInsertOneTable()

    val1name = "Olivier"
    val2firstname = "Maccaud"
    val3dob = "1889-04-20"
    val4wp = "Y"
    print(val1name + " | " + val2firstname + " | " + val3dob + " | " + val4wp)


    insert_records.insert_one_record_one_table("INSERT INTO T_Personne (id_personne, nom_pers, prenom_pers, date_de_naissance, possession_arme) VALUES (null, %(value1)s, %(value2)s, %(value3)s, %(value4)s)", val1name, val2firstname, val3dob, val4wp)


    connection.close_connection()
except Exception as critical_error:
    print("Critical Error : {0} ".format(critical_error))
