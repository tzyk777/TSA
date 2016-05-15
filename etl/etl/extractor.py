import abc
import csv


class Extractor(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractclassmethod
    def extract(self):
        return


class CSVExtractor(Extractor):
    def __init__(self, path, **kwargs):
        """
        :type path: str
        :type kwargs: dict
        """
        self.path = path
        self.delimiter = kwargs.get('delimiter', ',')
        self.quotechar = kwargs.get('quotechar', '|')

    def extract(self):
        with open(self.path, 'r', encoding="utf8") as csvfile:
            file = csv.reader(csvfile, delimiter=self.delimiter)
            for row in file:
                yield row


class QueryExtractor(Extractor):
    def __init__(self, query, db_conn):
        """
        :param table:
        :param query:
        :param db_conn
        """
        self.query = query
        self.db_conn = db_conn

    def extract(self):
        results = self.db_conn.get_values(self.query)
        for result in results:
            yield result


class MultiExtractor(Extractor):
    def __init__(self, extractors):
        """
        :param extractors: list[Extractor]
        """
        self.extractors = extractors

    def extract(self):
        for extractor in self.extractors:
            result = extractor.extract()
            yield result

