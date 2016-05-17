import json
import re
from collections import namedtuple, Counter
from nltk.corpus import stopwords
from etl.etl import *
from db.db import *

Feature = namedtuple('Feature', ['word', 'sentiment', 'frequency'])
my_words = ['url', 'im', 'day']
Stopwords = stopwords.words('english') + my_words


class FeatureTransformer(Transformer):
    def __init__(self):
        self.positive_counter = Counter()
        self.negative_counter = Counter()

    @staticmethod
    def replace(s):
        # look for 2 or more repetitions of character and replace with the character itself
        pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
        return pattern.sub(r"\1\1", s)

    @staticmethod
    def process_tweet(tweet):
        # process the tweets

        # Convert to lower case
        tweet = tweet.lower()
        # Convert www.* or https?://* to URL
        tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet)
        # Convert @username to AT_USER
        tweet = re.sub('@[^\s]+', 'AT_USER', tweet)
        # Remove additional white spaces
        tweet = re.sub('[\s]+', ' ', tweet)
        # Replace #word with word
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
        # trim
        tweet = tweet.strip('\'"')
        return tweet

    def get_features(self, tweet):
        features = []
        # split tweet into words
        words = tweet.split()
        for w in words:
            # replace two or more with two occurrences
            w = self.replace(w)
            # strip punctuation
            w = w.strip('\'"?,.')
            # check if the word stats with an alphabet
            val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
            # ignore if it is a stop word
            w = w.lower()
            if w in Stopwords or val is None or len(w) == 1:
                continue
            else:
                features.append(w)
        return features

    def transform(self, data):
        for sentiment, text in data:
            tweet = self.process_tweet(text)
            features = self.get_features(tweet)
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