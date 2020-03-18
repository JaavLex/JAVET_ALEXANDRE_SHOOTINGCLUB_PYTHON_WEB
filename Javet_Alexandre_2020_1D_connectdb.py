# connect_db.py
# Javet Alexandre - 18.03.2020 20:28
import pymysql
import pymysql.cursors

class DatabaseTools():
    def __init__(self):
        print("DatabaseTools")

    @property
    def connect_ma_bd(self):
        self.db = pymysql.connect(host='localhost',
                                  port=33060,
                                  user="root",
                                  password="Pomme",
                                  db="JAVET_ALEXANDRE_SHOOTINGCLUB_BD_104",
                                  cursorclass=pymysql.cursors.DictCursor)
        print("Successfully connected to DataBase")
        return self

    def close_connection (self):
        if self.connect_ma_bd.db:
            print("Closing DataBase")
            self.db.close()
