import abc


class Transformer(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractclassmethod
    def transform(self, data):
        return
