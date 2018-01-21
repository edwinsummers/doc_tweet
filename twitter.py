"""Twitter authentication functions"""

from os import umask
import json
from getpass import getpass
from twython import Twython


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


def load_tokens(file='credentials.json'):
    """Return Twython object using final OAuth tokens"""

    try:
        with open(file) as creds_file:
            credentials = json.load(creds_file)
    except FileNotFoundError:
        credentials = init_creds()

    consumer_key = credentials['consumer_key']
    consumer_secret = credentials['consumer_secret']
    oauth_token = credentials['oauth_token']
    oauth_token_secret = credentials['oauth_token_secret']

    return Twython(consumer_key, consumer_secret, oauth_token, oauth_token_secret)
