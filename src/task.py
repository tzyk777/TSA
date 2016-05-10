import json
import datetime as dt

from src.db import DBConnection
from src.extractor import Extractor
from src.loader import Loader
from src.queries import *


class Task:
    def __init__(self, date, table, db_conn, user_dates, config):
        """
        :type date: datetime.date
        :type table: str
        :type db_conn: DBConnection
        :type user_dates: dict[str, datetime.date]
        :type config: dict[str, Any]
        """
        self.date = date
        self.table = table
        self.db_conn = db_conn
        self.config = config
        self.extractor = Extractor(date, config['user_names'], config['twitter_auth'],
                                   user_dates, config['number_of_tweets'])
        self.loader = Loader(self.table, self.db_conn)

    def execute(self):
        data = self.extractor.get_tweets()
        self.loader.load(data)
        self.db_conn.query_table(self.table)


def main():
    date = dt.date.today()
    with open('config.json') as config_file:
        config = json.load(config_file)

    db_conn = DBConnection(config['db'])
    user_dates = {}
    usernames = config['user_names']
    table = 'tweets'
    for user in usernames:
        max_date = db_conn.get_value(get_max_value(table,
                                                   'post_time',
                                                   ['post_user'],
                                                   [user]))
        max_date = max_date[0] or dt.datetime(1970, 1, 1, 0, 0, 0)
        user_dates[user] = max_date
    task = Task(date, table, db_conn, user_dates, config)
    task.execute()

if __name__ == '__main__':
    main()