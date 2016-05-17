import abc


class Process(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractclassmethod
    def process(self):
        return


class QueryProcess(Process):
    """
    Query process before extractor.
    Usually it does some preparations, e.g clean up database table
    """
    def __init__(self, db_conn, query):
        """
        :param db_conn: db.db_conn
        :param query: db.queries
        """
        self.db_conn = db_conn
        self.query = query

    def process(self):
        self.db_conn.execute(str(self.query))
