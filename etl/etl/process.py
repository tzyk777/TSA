import abc


class Process(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractclassmethod
    def process(self):
        return


class QueryProcess(Process):
    def __init__(self, db_conn, query):
        """
        :type db_conn: db.db_conn
        :type query: db.queries
        """
        self.db_conn = db_conn
        self.query = query

    def process(self):
        self.db_conn.execute(str(self.query))
