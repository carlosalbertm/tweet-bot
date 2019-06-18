"""
    Tweet bot API
    Author: Carlos
    Version: 1.0

"""

from twython import Twython
from settings import {
    APP_KEY,
    APP_SECRET,
    OAUTH_TOKEN,
    OAUTH_TOKEN_SECRET,
}

APP_KEY = 'YOUR_APP_KEY'
APP_SECRET = 'YOUR_APP_SECRET'

twitter = Twython(APP_KEY, APP_SECRET)

auth = twitter.get_authentication_tokens(callback_url='http://mysite.com/callback')
