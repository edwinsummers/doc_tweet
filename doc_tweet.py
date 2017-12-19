#!/usr/bin/env python
"""Compose and tweet your daily #100DaysOfCode update"""


from sys import argv
import json
from datetime import datetime
from twython import Twython


START_DATE = datetime(2017, 12, 10)
HASHTAG = '#100DaysOfCode'
DAY_PREFIX = 'D'


def compute_day():
    """Return integer representing increment since start date

    Per good indexing, the start date is considered day 0 :)"""

    elapsed = datetime.today() - START_DATE
    return elapsed.days


def compose_tweet(message):
    """Return text to tweet by prefixing date index and hashtag"""

    prefix = '{0}{1}'.format(DAY_PREFIX, compute_day())
    tweet = '{0} {1} {2}'.format(prefix, message, HASHTAG)
    return tweet


def get_oauth_tokens(credentials):
    """Return Twython object and OAuth tokens from user authentication"""

    t = Twython(credentials['consumer_key'], credentials['consumer_secret'])
    auth = t.get_authentication_tokens()
    oauth_token = auth['oauth_token']
    oauth_token_secret = auth['oauth_token_secret']

    print('Please authenticate to Twitter at: {}'.format(auth['auth_url']))

    oauth_verifier = input('Enter PIN code: ')
    t = Twython(credentials['consumer_key'],
                credentials['consumer_secret'],
                oauth_token,
                oauth_token_secret,
               )
    tokens = t.get_authorized_tokens(oauth_verifier)
    t = Twython(credentials['consumer_key'],
                credentials['consumer_secret'],
                tokens['oauth_token'],
                tokens['oauth_token_secret'],
               )
    return (t, tokens)


def load_tokens():
    """Return Twython object using final OAuth tokens"""

    with open('secrets/app_keys.json') as app_file, open('secrets/oauth_tokens.json') as token_file:
        app = json.load(app_file)
        tokens = json.load(token_file)

    consumer_key = app['consumer_key']
    consumer_secret = app['consumer_secret']
    oauth_token = tokens['oauth_token']
    oauth_token_secret = tokens['oauth_token_secret']

    return Twython(consumer_key, consumer_secret, oauth_token, oauth_token_secret)


def main():
    """Main"""

    if len(argv) < 2:
        exit('ERROR: A message was not provided')
    message = argv[1]

    twitter = load_tokens()
    tweet = compose_tweet(message)
    print('Sending {} character status update...'.format(len(tweet)))
    print()
    print(twitter.update_status(status=tweet))


if __name__ == '__main__':
    main()
