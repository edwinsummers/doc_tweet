#!/usr/bin/env python
"""Compose and tweet your daily #100DaysOfCode update"""


from os import umask
from sys import argv
import json
from datetime import datetime
from getpass import getpass
from twython import Twython


START_DATE = datetime(2018, 1, 10)
HASHTAG = '#100DaysOfCode'
DAY_PREFIX = 'D'


def init_creds():
    """Create credentials json file"""

    credentials = {}

    print('You do not appear to have credentials for this app yet.')
    print('Please register your app at https://apps.twitter.com')
    credentials['consumer_key'] = input('Enter the consumer key: ')
    credentials['consumer_secret'] = getpass('Enter the consumer secret: ')
    credentials.update(get_oauth_tokens(credentials))
    umask(int('277', 8))
    with open('credentials.json', 'x') as f_out:
        json.dump(credentials, f_out)

    return credentials


def get_oauth_tokens(credentials):
    """Return user OAuth tokens from user authentication"""

    twitter = Twython(credentials['consumer_key'],
                      credentials['consumer_secret'])
    auth = twitter.get_authentication_tokens()
    oauth_token = auth['oauth_token']
    oauth_token_secret = auth['oauth_token_secret']

    print('Please authenticate to Twitter at: {}'.format(auth['auth_url']))

    oauth_verifier = input('Enter PIN code: ')
    twitter = Twython(credentials['consumer_key'],
                      credentials['consumer_secret'],
                      oauth_token,
                      oauth_token_secret,
                     )
    tokens = twitter.get_authorized_tokens(oauth_verifier)

    return tokens


def load_tokens():
    """Return Twython object using final OAuth tokens"""

    try:
        with open('credentials.json') as creds_file:
            credentials = json.load(creds_file)
    except FileNotFoundError:
        credentials = init_creds()

    consumer_key = credentials['consumer_key']
    consumer_secret = credentials['consumer_secret']
    oauth_token = credentials['oauth_token']
    oauth_token_secret = credentials['oauth_token_secret']

    return Twython(consumer_key, consumer_secret, oauth_token, oauth_token_secret)


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


def main():
    """Main"""

    if len(argv) < 2:
        exit('Usage: {0} <message>'.format(argv[0]))
    message = argv[1]

    twitter = load_tokens()
    tweet = compose_tweet(message)
    print('Sending {} character status update...'.format(len(tweet)))
    print()
    result = twitter.update_status(status=tweet)
    print('Set status update for user {0} to: {1}'.format(
        result['user']['name'], result['text']))


if __name__ == '__main__':
    main()
