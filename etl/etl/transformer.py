import abc


class Transformer(object):
    """
    Transform data in correct format
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractclassmethod
    def transform(self, data):
        return
