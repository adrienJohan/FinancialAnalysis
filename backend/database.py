import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="ton_mot_de_passe",
                database="test_db"
            )
            self.cursor = self.conn.cursor()
            print("Connexion réussie à MySQL")
        except Error as e:
            print(f"Erreur de connexion à MySQL : {e}")

    def close(self):
        self.cursor.close()
        self.conn.close()
