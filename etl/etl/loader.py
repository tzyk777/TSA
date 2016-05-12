import abc

from db.db import InsertQuery


class Loader(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractclassmethod
    def load(self, data):
        return


class DBLoader(Loader):
    def __init__(self, table, columns, db_conn):
        """
        :type table: str
        :type columns: list[str]
        :type db_conn: db
        """
        self.table = table
        self.columns = columns
        self.db_conn = db_conn

    def load(self, data):
        """
        :type data: collections.Iterator[Any]
        :rtype: int
        """
        numbers = 0
        for numbers, line in enumerate(data, start=1):
            query = InsertQuery(self.table, self.columns, list(line))
            self.db_conn.execute(str(query))
        return numbers
