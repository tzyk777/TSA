"""
Things to improve:
- address the same word appears more than once in a text. Now if it appears
more than once, we only count one.
"""
import json
import functools

from etl.etl import *
from db.db import *
from utils import process_tweet, get_features


class NaiveBayes:
    def __init__(self, db_conn):
        """
        :param db_conn: db.DBConnection
        """
        self.db_conn = db_conn
        self.num_positive = 0
        self.num_negative = 0
        self.pos_prob = 0
        self.neg_prob = 0
        self.pos_feature_prob = {}
        self.neg_feature_prob = {}

    def train_model(self):
        self.num_positive = self.db_conn.get_value("select count(*) from features where sentiment = 'Positive'")[0]
        self.num_negative = self.db_conn.get_value("select count(*) from features where sentiment = 'Negative'")[0]
        self.pos_prob = (self.num_positive/(self.num_positive+self.num_negative))
        self.neg_prob = (self.num_negative/(self.num_positive+self.num_negative))

        data = self.db_conn.get_values(SelectQuery('features'))
        for line in data:
            sentiment, word, frequency = line
            if sentiment == 'Positive':
                self.pos_feature_prob[word] = frequency/self.num_positive
            elif sentiment == 'Negative':
                self.neg_feature_prob[word] = frequency/self.num_negative

    def classify(self, text):
        """
        :param text: str
        :return: str
        """
        good_text = process_tweet(text)
        features = get_features(good_text)
        if not features:
            return None
        pos_feature_matrix = [self.pos_feature_prob.get(feature, 1/self.num_positive) for feature in features]
        neg_feature_matrix = [self.neg_feature_prob.get(feature, 1/self.num_negative) for feature in features]
        positive_prob = self.pos_prob * functools.reduce(lambda x, y: x*y, pos_feature_matrix)
        negative_prob = self.neg_prob * functools.reduce(lambda x, y: x*y, neg_feature_matrix)

        # what if positive_prob = negative_prob
        return 'Positive' if positive_prob > negative_prob else 'Negative'


class ClassificationTransformer(Transformer):
    def __init__(self, classifier):
        """
        :param classifier: NaiveBayes
        """
        self.classifier = classifier

    def transform(self, data):
        """
        :param data: collection.iterator[Any]
        :return: list[str]
        """
        for line in data:
            dt, post_user, post_time, content = line
            sentiment = self.classifier.classify(content)
            if sentiment:
                yield [dt, post_user, post_time, content, sentiment]


class ClassificationTask(Task):
    def __init__(self, config):
        """
        :param config: dict[str, any]
        """
        self.config = config
        self.db_conn = DBConnection(config['db'])
        self.classifier = NaiveBayes(self.db_conn)
        self.path = 'D:\programming\TSA\classifications.csv'
        classifier = NaiveBayes(self.db_conn)
        classifier.train_model()
        extractor = QueryExtractor(SelectQuery('tweets'), self.db_conn)
        transformer = ClassificationTransformer(classifier)
        loader = PDLoader(self.path)
        super().__init__(extractor, transformer, loader)

    def before_execute(self):
        print('Executing classification job')

    def after_execute(self):
        print('Finished classification job')

    def before_extract(self):
        print('Extract unlabeled samples from tweets')

    def after_extract(self):
        print('Extracted all the unlabeled samples')

    def before_transform(self):
        print('Classifying samples')

    def after_transform(self):
        print('Classified all the samples')

    def before_load(self):
        print('Loading labeled samples to file {file}'.format(file=self.path))


def main():
    with open('D:\programming\TSA\config.json') as config_file:
        config = json.load(config_file)

    ClassificationTask(config).execute()

if __name__ == '__main__':
    main()
