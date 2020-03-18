# insert_one_table.py
# Javet Alexandre - 18.03.2020 20:28
import pymysql
import Javet_Alexandre_2020_1D_connectdb


class DbInsertOneTable():

    def __init__(self):
        self.connection_dbc = Javet_Alexandre_2020_1D_connectdb.DatabaseTools().connect_ma_bd
        self.DBcursor = self.connection_dbc.db.cursor()
        print("")

    def insert_one_record_one_table(self, requete_insert_mysql, insert1, insert2, insert3, insert4):
        # Ouch le code ↓, mais c'est vous le boss je laisse comme ça...
        try:
            self.DBcursor.execute(requete_insert_mysql, {'value1': insert1, 'value2': insert2, 'value3': insert3, 'value4': insert4})
            self.connection_dbc.db.commit()()
            self.DBcursor.close()
        except pymysql.DataError as error1:
            self.connection_dbc.db.rollback()
            print(" DataError occurred : %s", error1)
            print("connection_dbc.db.rollback() insertOneRecord")
        except pymysql.IntegrityError as error5:
            self.connection_dbc.db.rollback()
            print(" IntegrityError occurred : %s", error5)
            print("connection_dbc.db.rollback() insertOneRecord")
        except pymysql.DatabaseError as error2:
            self.connection_dbc.db.rollback()
            print(" DatabaseError occurred : %s", error2)
            print("connection_dbc.db.rollback() insertOneRecord")
        except pymysql.Error as error:
            self.connection_dbc.db.rollback()
            print(" Error occurred : %s", error)
            print("connection_dbc.db.rollback() insertOneRecord")
        except pymysql.Warning as error3:
            self.connection_dbc.db.rollback()
            print(" Warning : %s", error3)
            print("connection_dbc.db.rollback() insertOneRecord")
        except pymysql.MySQLError as error4:
            self.connection_dbc.db.rollback()
            print(" MySQLError occurred : %s", error4)
            print("connection_dbc.db.rollback() insertOneRecord")
        except:
            self.connection_dbc.db.rollback()
            print("Unknown error occurred")
        finally:
            print("Process ended....finally self.DBcursor.close()")
            self.DBcursor.close()
