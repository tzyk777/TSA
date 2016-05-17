import tweepy
from collections import namedtuple

Tweet_row = namedtuple('Tweet_row', 'dt post_user post_time content attitude')


class Extractor:
    def __init__(self, date, user_names, twitter_config, user_dates, number_of_tweets=100):
        """
        :type date datetime.date
        :type usernames: list
        :type twitter_config: dict[str, str]
        :type user_dates: dict[str, datetime.date]
        :type number_of_tweets: int
        """
        self.date = date
        self.user_names = user_names
        self.config = twitter_config
        self.user_dates = user_dates
        self.number_of_tweets = number_of_tweets

        consumer_key = self.config['consumer_key']
        consumer_secret = self.config['consumer_secret']
        access_key = self.config['access_key']
        access_secret = self.config['access_secret']

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        self.api = tweepy.API(auth)

    def get_tweets(self):
        for user in self.user_names:
            max_date = self.user_dates[user]
            tweets = self.api.user_timeline(screen_name=user, count=self.number_of_tweets)
            for tweet in tweets:
                if tweet.created_at > max_date:
                    yield Tweet_row(
                        dt=self.date,
                        post_user=user,
                        post_time=tweet.created_at,
                        content=tweet.text,
                        attitude='P'
                    )

