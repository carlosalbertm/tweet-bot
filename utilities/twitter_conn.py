"""Module providing a function to manage twitter api connection"""

import tweepy

from files import get_name_girl
from settings import *


def get_client_v2() -> tweepy.Client:
    """Function initialize twiter API."""
    return tweepy.Client(
        bearer_token=settings.BEARER_TOKEN,
        consumer_key=settings.CONSUMER_KEY,
        consumer_secret=settings.CONSUMER_SECRET,
        access_token=settings.ACCESS_TOKEN,
        access_token_secret=settings.ACCESS_TOKEN_SECRET,
    )


def get_twitter_conn_v1() -> tweepy.API:
    """Get twitter conn 1.1"""

    auth = tweepy.OAuth1UserHandler(
        settings.CONSUMER_KEY,
        settings.CONSUMER_SECRET,
    )
    auth.set_access_token(
        settings.ACCESS_TOKEN,
        settings.ACCESS_TOKEN_SECRET,
    )
    return tweepy.API(auth)


def upload_single_file(image):
    """Function upload a file using twiter API."""
    client_v1 = get_twitter_conn_v1()

    girl_name = get_name_girl(image)
    if girl_name in settings.tweets:
        image_url = f"${settings.ROUTE}/${image}"
        try:
            media = client_v1.media_upload(filename=image_url)
            media_id = media.media_id
        except tweepy.errors.Forbidden as e:
            print(e)

    return media_id


def upload_multiple_files(files):
    """Function upload multiple files using twiter API."""
    media_ids = []
    image_to_delete = []
    base_name = get_name_girl(files[0])

    for index in range(settings.IMAGE_BATCH_SIZE):
        current_name = get_name_girl(files[index])
        if base_name is current_name:
            print(f"name {current_name}, index {index}")
            media_id = upload_single_file(files[index])
            image_to_delete.append(files[index])
            media_ids.append(media_id)

    return [media_ids, image_to_delete]
