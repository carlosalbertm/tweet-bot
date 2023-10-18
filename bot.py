"""
    Tweet bot API
    Author: Carlos
    Version: 1.5

"""

import time
from datetime import datetime
import pytz

import tweepy
from apscheduler.schedulers.background import BackgroundScheduler
from settings import config
from utilities.files import get_files_by_size, get_name_girl, delete_images_tweeted
from utilities.twitter_conn import upload_multiple_files, get_client_v2


def tweet_scheduled():
    """Main function to post simple tweets"""
    mex_time = pytz.timezone('Japan')

    client = get_client_v2()
    # print(client.get_me())

    files = get_files_by_size(config.ROUTE)
    image = files[0]
    girl_name = get_name_girl(image)
    if girl_name in config.tweets:
        try:
            data_media = upload_multiple_files(files)
            media_ids = data_media[0]
            images_for_delete = data_media[1]
            print(media_ids)

            tweet = config.tweets[girl_name]
            if media_ids:
                response = client.create_tweet(text=tweet, media_ids=media_ids)
                currtent_time = datetime.now(mex_time).strftime("%H:%M:%S")
                print(f'https://twitter.com/user/status/{response.data["id"]}')
                print(
                    f'tweeted -> {girl_name} image has been posted at {currtent_time}'
                )
                delete_images_tweeted(images_for_delete)
        except (tweepy.errors.Forbidden, tweepy.errors.HTTPException) as tweepy_error:
            print(f'Internal error {tweepy_error}')
    else:
        print(f'Missing girl {girl_name}')


if __name__ == "__main__":
    scheduler = BackgroundScheduler({'apscheduler.timezone': 'UTC'})
    scheduler.add_job(tweet_scheduled, 'interval', seconds=55)
    scheduler.start()

    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit) as system_error:
        scheduler.shutdown()
        raise system_error
    # main()
