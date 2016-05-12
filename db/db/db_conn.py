import sys
import psycopg2


class DBConnection:
    def __init__(self, db_config):
        """
        :type db_config: dict
        """
        host = db_config['host']
        dbname = db_config['dbname']
        user = db_config['user']
        password = db_config['password']

        conn_string = "host='{host}' dbname='{dbname}' user='{user}' password='{password}'".\
            format(host=host, dbname=dbname, user=user, password=password)

        try:
            conn = psycopg2.connect(conn_string)
        except psycopg2.Error as e:
            print("Unable to connect!")
            print(e.pgerror)
            print(e.diag.message_detail)
            sys.exit(1)
        else:
            conn.autocommit = True
            self.cursor = conn.cursor()

    def close_connection(self):
        self.cursor.close()

    def get_value(self, query):
        """
        :type query: db.queries
        :rtype: any
        """
        try:
            self.cursor.execute(str(query))
            result = self.cursor.fetchone()
        except psycopg2.Error as e:
            print("Error happened during reading")
            print(e.pgerror)
            print(e.diag.message_detail)
        else:
            return result

    def get_values(self, query):
        """
        :type query: db.queries
        :rtype: list[any]
        """
        try:
            self.cursor.execute(str(query))
            results = self.cursor.fetchall()
        except psycopg2.Error as e:
            print("Error happened during reading")
            print(e.pgerror)
            print(e.diag.message_detail)
        else:
            return results

    def execute(self, query):
        """
        :type query: db.queries
        """
        try:
            self.cursor.execute(str(query))
        except psycopg2.Error as e:
            print("Error happened during insertion")
            print(e.pgerror)
            print(e.diag.message_detail)


