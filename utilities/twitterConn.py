import tweepy

from settings import config
from files import get_name_girl


def get_client_v2() -> tweepy.Client:
    return tweepy.Client(
        bearer_token=config.BEARER_TOKEN,
        consumer_key=config.CONSUMER_KEY,
        consumer_secret=config.CONSUMER_SECRET,
        access_token=config.ACCESS_TOKEN,
        access_token_secret=config.ACCESS_TOKEN_SECRET,
    )


def get_twitter_conn_v1() -> tweepy.API:
    """Get twitter conn 1.1"""

    auth = tweepy.OAuth1UserHandler(
        config.CONSUMER_KEY,
        config.CONSUMER_SECRET,
    )
    auth.set_access_token(
        config.ACCESS_TOKEN,
        config.ACCESS_TOKEN_SECRET,
    )
    return tweepy.API(auth)


def upload_single_file(image):
    client_v1 = get_twitter_conn_v1()

    girl_name = get_name_girl(image)
    if girl_name in config.tweets:
        image_url = f"${config.ROUTE}/${image}"
        try:
            """Upload image"""
            media = client_v1.media_upload(filename=image_url)
            media_id = media.media_id
        except tweepy.errors.Forbidden as e:
            print(e)

    return media_id


def upload_multiple_files(files):
    media_ids = []
    image_to_delete = []
    base_name = get_name_girl(files[0])

    for index in range(config.IMAGE_BATCH_SIZE):
        current_name = get_name_girl(files[index])
        if base_name is current_name:
            print(f"name {current_name}, index {index}")
            media_id = upload_single_file(files[index])
            image_to_delete.append(files[index])
            media_ids.append(media_id)

    return [media_ids, image_to_delete]
