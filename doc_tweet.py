#!/usr/bin/env python
"""Compose and tweet your daily #100DaysOfCode update"""


from datetime import datetime

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


