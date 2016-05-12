import abc


class Transformer(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractclassmethod
    def transformer(self, data):
        return
