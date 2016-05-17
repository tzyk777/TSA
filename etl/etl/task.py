import abc


class Task(object):
    """
    Task abstract class
    Control etl work flow
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, extractor, transformer, loader, pre_process=None, post_process=None):
        """
        :param extractor: etl.Extractor
        :param transformer: etl.Transformer
        :param loader: etl.Loader
        :param pre_process: etl.Process
        :param post_process: etl.Process
        """
        self.extractor = extractor
        self.transformer = transformer
        self.loader = loader
        self.pre_process = pre_process
        self.post_process = post_process

    def execute(self):
        self.before_execute()
        self.before_extract()
        if self.pre_process:
            self.pre_process.process()
        data = self.extractor.extract()
        self.after_extract()
        self.before_transform()
        data = self.transformer.transform(data)
        self.after_transform()
        self.before_load()
        numbers = self.loader.load(data)
        self.after_load(numbers)
        if self.post_process:
            self.post_process.process()
        self.after_execute()

    @abc.abstractclassmethod
    def before_execute(self):
        return

    @abc.abstractclassmethod
    def after_execute(self):
        return

    @abc.abstractclassmethod
    def before_extract(self):
        return

    @abc.abstractclassmethod
    def after_extract(self):
        return

    @abc.abstractclassmethod
    def before_transform(self):
        return

    @abc.abstractclassmethod
    def after_transform(self):
        return

    @abc.abstractclassmethod
    def before_load(self):
        return

    @staticmethod
    def after_load(numbers):
        print('{} records are loaded'.format(numbers))
        return
