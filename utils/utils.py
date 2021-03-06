import re
from nltk.corpus import stopwords

my_words = ['url', 'im', 'day']
Stopwords = stopwords.words('english') + my_words


def replace(s):
    # look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)


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


def get_features(tweet):
    features = []
    # split tweet into words
    words = tweet.split()
    for w in words:
        # replace two or more with two occurrences
        w = replace(w)
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
