import json
from collections import namedtuple

from db.db import *
from etl.etl import *

Sample = namedtuple('Sample', ['sentiment', 'sample'])


class SampleTransformer(Transformer):
    def transform(self, data):
        next(data)
        for line in data:
            if line[1] == '0':
                sentiment = 'Negative'
            elif line[1] == '1':
                sentiment = 'Positive'

            yield Sample(
                sentiment=sentiment,
                sample=line[3].strip().replace('"', '').replace("'", '')
            )


class SampleTask(Task):
    table = 'samples'

    def __init__(self, config):
        """
        :type config: dict
        """
        db_conn = DBConnection(config['db'])
        file_path = "D:\programming\dataset\Sentiment_Analysis_Dataset.csv"
        pre_process = QueryProcess(db_conn, DeleteQuery(self.table))
        extractor = CSVExtractor(file_path)
        transformer = SampleTransformer()
        loader = DBLoader(self.table, Sample._fields, db_conn)
        super().__init__(extractor, transformer, loader, pre_process=pre_process)


def main():
    with open('D:\programming\TSA\src\config.json') as config_file:
        config = json.load(config_file)

    SampleTask(config).execute()

if __name__ == '__main__':
    main()
