class Loader:
    def __init__(self, table, db_conn):
        """
        :type table: str
        :type db_conn: connection
        """
        self.table = table
        self.db_conn = db_conn

    def load(self, data):
        """
        :type data: iter[Tweet_row]
        """
        numbers = 0
        for numbers, tweet in enumerate(data, start=1):
            columns = tweet._fields
            self.db_conn.insert_row(self.table, columns, tweet)
        print("Inserted {numbers} rows".format(numbers=numbers))
