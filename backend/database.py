import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="fletuser",
                password="fletpassword",
                database="fletdb"
            )
            self.cursor = self.conn.cursor()
            print("Connexion réussie à MySQL")
        except Error as e:
            print(f"Erreur de connexion à MySQL : {e}")

    def query(self, sql, params=None, fetch=True):
        """
        Exécute une requête SQL.
        :param sql: La requête SQL à exécuter (str)
        :param params: Les paramètres pour la requête (tuple ou list, optionnel)
        :param fetch: Si True, retourne les résultats (pour SELECT), sinon None (pour INSERT/UPDATE/DELETE)
        :return: Liste de résultats (si fetch=True) ou None
        """
        try:
            # Exécute la requête avec les paramètres (s'ils existent)
            if params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)

            # Si c'est une requête de lecture (SELECT)
            if fetch:
                result = self.cursor.fetchall()
                return result
            # Si c'est une modification (INSERT, UPDATE, DELETE)
            else:
                self.conn.commit()
                return None

        except Error as e:
            print(f"Erreur lors de l'exécution de la requête : {e}")
            return None

    def close(self):
        self.cursor.close()
        self.conn.close()