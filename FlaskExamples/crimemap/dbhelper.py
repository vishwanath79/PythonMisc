import pymysql
import dbconfig

class DBHelper:

    def connect(self,database="crimemap"):
        return pymysql.connect(host="localhost",user=dbconfig.db_user,passwd=dbconfig.db_password,db=database)

    def get_all_inputs(self):
        connection = self.connect()
        try:
            query = "select description from crimes;"
            with connection.cursor() as cursor:
                cursor.execute(query)
            return cursor.fetchall()
        finally:
            connection.close()

    def add_input(self,data):
        connection = self.connect()
        try:
            query = "iNSERT into crimes (description) VALUES ('{}');".format(data)
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
        finally:
            connection.close()


    def clear_all(self):
        connection = self.connect()
        try:
            query = "delete from crimes;"
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
        finally:
            connection.close()


    def add_crime(self,category,date,latitude,longitude, description):
        connection = self.connect()
        try:
            query = "INSERT into crimes (category,date, latitude, longitude, description) VALUES (%s, %s, %s, %s, %s) "
            with connection.cursor() as cursor:
                cursor.execute(query, (category,date,latitude,longitude,description))
                connection.commit()
        except Exception as e:
            print(e)
        finally:
            connection.close()

