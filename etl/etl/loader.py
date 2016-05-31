import abc
import csv
import pandas as pd

from db.db import InsertQuery, SelectQuery


class Loader(object):
    """
    Load good data to the destination
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractclassmethod
    def load(self, data):
        return


class DBLoader(Loader):
    def __init__(self, table, columns, db_conn):
        """
        :param table: str
        :param columns: list[str]
        :param db_conn: db
        """
        self.table = table
        self.columns = columns
        self.db_conn = db_conn

    def load(self, data):
        """
        :param data: collections.Iterator[Any]
        :return: int
        """
        numbers = 0
        for numbers, line in enumerate(data, start=1):
            query = InsertQuery(self.table, self.columns, list(line))
            self.db_conn.execute(str(query))
        return numbers


class CSVLoader(Loader):
    def __init__(self, path):
        """
        :param path: str
        """
        self.path = path

    def load(self, data):
        """
        :param data: collections.Iterator[Any]
        :return: int
        """
        with open(self.path, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            numbers = 0
            for numbers, line in enumerate(data, start=1):
                print(line)
                writer.writerow(line)
        return numbers


class PDLoader(Loader):
    def __init__(self, path):
        """
        :param path:
        """
        self.path = path

    def load(self, data):
        df = pd.DataFrame(data)
        df.to_csv(self.path)


class UpsertLoader(Loader):
    def __init__(self, table, db_conn, keys):
        """
        :param table: str
        :param db_conn: db
        :param keys:
        """
        self.table = table
        self.db_conn = db_conn
        self.keys = keys

    def load(self, data):
        """
        :param data:
        :return:
        """
        numbers = 0
        for numbers, line in enumerate(data, start=1):
            values = [getattr(line, key) for key in self.keys]
            query = SelectQuery(self.table, predicts=self.keys, values=values)
            value = self.db_conn.get_value(query)

