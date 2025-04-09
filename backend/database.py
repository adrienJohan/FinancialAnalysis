import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="iantsogod",
                password="nahida",
                database="fastapi"
            )
            self.cursor = self.conn.cursor()
            print("Connexion réussie à MySQL")
        except Error as e:
            print(f"Erreur de connexion à MySQL : {e}")

    def close(self):
        self.cursor.close()
        self.conn.close()
