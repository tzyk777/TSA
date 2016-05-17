import abc
import csv


class Extractor(object):
    """
    Extract data from source
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractclassmethod
    def extract(self):
        return


class CSVExtractor(Extractor):
    """
    Extract data from csv file
    """
    def __init__(self, path, **kwargs):
        """
        :param path: str
        :param kwargs: dict
        """
        self.path = path
        self.delimiter = kwargs.get('delimiter', ',')
        self.quotechar = kwargs.get('quotechar', '|')

    def extract(self):
        """
        :return: list[str]
        """
        with open(self.path, 'r', encoding="utf8") as csvfile:
            file = csv.reader(csvfile, delimiter=self.delimiter)
            for row in file:
                yield row


class QueryExtractor(Extractor):
    def __init__(self, query, db_conn):
        """
        :param table: str
        :param query: db.queries
        :param db_conn: db.DBConnection
        """
        self.query = query
        self.db_conn = db_conn

    def extract(self):
        """
        :return: list[str]
        """
        results = self.db_conn.get_values(self.query)
        for result in results:
            yield result


class MultiExtractor(Extractor):
    """
    Extract data from multiple sources
    """
    def __init__(self, extractors):
        """
        :param extractors: list[Extractor]
        """
        self.extractors = extractors

    def extract(self):
        """
        :return:
        """
        for extractor in self.extractors:
            result = extractor.extract()
            yield result

