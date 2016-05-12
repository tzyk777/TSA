import abc
import csv


class Extractor(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractclassmethod
    def extractor(self):
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
