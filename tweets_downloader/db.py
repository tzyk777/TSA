import sys
import psycopg2


class DBConnection:
    def __init__(self, db_config):
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

    def get_connection(self):
        return self.cursor

    def close_connection(self):
        self.cursor.close()

    def get_value(self, query):
        try:
            self.cursor.execute(query)
            results = self.cursor.fetchone()
        except psycopg2.Error as e:
            print("Error happened during reading")
            print(e.pgerror)
            print(e.diag.message_detail)
        else:
            return results

    def query_table(self, table):
        """
        :type table: str
        :rtype: list[list[str]]
        """
        query = "SELECT * FROM {table}".format(table=table)
        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()
        except psycopg2.Error as e:
            print("Error happened during reading")
            print(e.pgerror)
            print(e.diag.message_detail)
        else:
            return results

    def insert_row(self, table, columns, values):
        """
        :type table: str
        :type columns: list
        :type values: list
        """
        query = "INSERT INTO {table}({columns}) VALUES {values}"\
            .format(table=table,
                    columns=','.join(c for c in columns),
                    values=tuple([str(v).strip().replace("'", '').replace('"', '') for v in values]))
        try:
            print(query)
            self.cursor.execute(query)
        except psycopg2.Error as e:
            print("Error happened during insertion")
            print(e.pgerror)
            print(e.diag.message_detail)


