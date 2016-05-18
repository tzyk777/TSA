import json
from collections import namedtuple, Counter
from etl.etl import *
from db.db import *
from utils import process_tweet, get_features

Feature = namedtuple('Feature', ['word', 'sentiment', 'frequency'])


class FeatureTransformer(Transformer):
    def __init__(self):
        self.positive_counter = Counter()
        self.negative_counter = Counter()

    def transform(self, data):
        for sentiment, text in data:
            tweet = process_tweet(text)
            features = get_features(tweet)
            if sentiment.lower() == 'positive':
                self.positive_counter.update(features)
            elif sentiment.lower() == 'negative':
                self.negative_counter.update(features)
            else:
                print('Unknown label {label}'.format(label=sentiment))

        for word, frequency in self.positive_counter.items():
            yield Feature(
                word=word,
                sentiment='Positive',
                frequency=frequency,
            )

        for word, frequency in self.negative_counter.items():
            yield Feature(
                word=word,
                sentiment='Negative',
                frequency=frequency,
            )


class FeatureTask(Task):
    table = 'features'

    def __init__(self, config):
        """
        :param config:
        """
        db_conn = DBConnection(config['db'])
        pre_process = QueryProcess(db_conn, DeleteQuery(self.table))
        extractor = QueryExtractor(SelectQuery('samples'), db_conn)
        transformer = FeatureTransformer()
        loader = DBLoader(self.table, Feature._fields, db_conn)
        super().__init__(extractor, transformer, loader, pre_process=pre_process)

    def before_execute(self):
        print('Executing features extraction job')

    def after_execute(self):
        print('Finished features extraction job')

    def before_extract(self):
        print('Extracting samples from table {table}'.format(table='samples'))

    def after_extract(self):
        print('Extracted all the samples')

    def before_transform(self):
        print('Transforming samples, counting frequency')

    def after_transform(self):
        print('Transformed all the samples')

    def before_load(self):
        print('Loading data to table {table}'.format(table=self.table))


def main():
    with open('D:\programming\TSA\config.json') as config_file:
        config = json.load(config_file)

    FeatureTask(config).execute()

if __name__ == '__main__':
    main()