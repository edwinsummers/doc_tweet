#!/usr/bin/env python
"""Compose and tweet your daily #100DaysOfCode update"""


from sys import argv
import json
from datetime import date
from dateutil.parser import parse
import twitter


def load_config(filename):
    """Load JSON-formatted file and return contents"""

    with open(filename, 'r') as f_in:
        contents = json.load(f_in)
    contents['start_date'] = parse(contents['start_date'])
    return contents


def init_config(config='config.json'):
    """Initialize config file with user inputs"""

    start_date = None
    hashtag = None
    print('Initializing configuration file')
    print()
    while not start_date:
        start_input = input('Enter starting date [{}]: '
                            .format(date.today().isoformat()))
        if not start_input:
            start_date = date.today()
        else:
            try:
                start_date = parse(start_input)
            except ValueError:
                print('Please enter date in MM/DD/YYYY format.')

    while not hashtag:
        hashtag_input = input('Enter hashtag to use [#100DaysOfCode]: ')
        if not hashtag_input:
            hashtag = '#100DaysOfCode'
        else:
            if (hashtag_input.startswith('#') and hashtag_input[1:].isalnum()):
                hashtag = hashtag_input
            else:
                print('Hashtags must start with "#" and contain only'
                      'alphanumeric characters.')

    output = {'start_date': start_date.isoformat(), 'hashtag': hashtag,}
    with open(config, 'x') as f_out:
        json.dump(output, f_out)
    print('Config initialization saved to {}'.format(config))
    return {'start_date': start_date, 'hashtag': hashtag}


def main():
    """Main"""

    config = 'config.json'

    if len(argv) < 2:
        exit('Usage: {0} <message>'.format(argv[0]))
    message = argv[1]

    try:
        user_prefs = load_config(config)
    except FileNotFoundError:
        print('Config file not found.')
        user_prefs = init_config(config)

    twit_user = twitter.load_tokens()
    day_index = (date.today() - user_prefs['start_date'].date()).days
    tweet = 'D{0} {1} {2}'.format(day_index, message, user_prefs['hashtag'])
    print('Preparing to send the following status update:')
    print(tweet)
    acknowledge = input('Send status update? [y|N]: ')
    if 'y' in acknowledge.lower():
        print('Sending {} character status update...'.format(len(tweet)))
        print()
        result = twit_user.update_status(status=tweet)
        print('Set status update for user {0} to: {1}'.format(
            result['user']['name'], result['text']))
    else:
        print('Update not sent')


if __name__ == '__main__':
    main()
