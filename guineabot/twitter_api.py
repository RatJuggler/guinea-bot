import logging
import os
import re
import tweepy


def create_twitter_api():
    consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
    consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as error:
        logging.error("Error creating Twitter API!", error)
        raise error
    return api


def tweet(message, api=None):
    if not api:
        api = create_twitter_api()
    try:
        api.update_status(message)
        logging.info("Tweeted: {0}".format(message))
    except tweepy.TweepError as error:
        if error.api_code == 187:
            logging.warning("Duplicate tweet discarded!")
        else:
            logging.error("Error trying to tweet!", error)
            raise error


def tweet_with_photo(message, photo, api=None):
    if not api:
        api = create_twitter_api()
    try:
        media = api.media_upload(photo)
        api.update_status(message, media_ids=[media.media_id])
        logging.info("Tweeted: {0} {1}".format(message, photo))
    except tweepy.TweepError as error:
        if error.api_code == 187:
            logging.warning("Duplicate photo tweet discarded!")
        else:
            logging.error("Error trying to tweet with photo!", error)
            raise error


def get_current_friends(api=None):
    if not api:
        api = create_twitter_api()
    return api.friends_ids()


def good_name(name):
    return re.search(r"guinea\s*pig", name, re.IGNORECASE)


def find_new_friend(friends, api=None):
    page_no = 0
    if not api:
        api = create_twitter_api()
    if not friends or len(friends) == 0:
        logging.warning("Expected more friends: {0}".format(friends))
        friends = get_current_friends(api)
    while page_no < 100:
        page = api.search_users("guinea pig", 20, page_no)
        for new_friend in page:
            if new_friend.id not in friends and (good_name(new_friend.name) or good_name(new_friend.screen_name)):
                new_friend.follow()
                friends.append(new_friend.id)
                tweet("I've decided to follow {0}.".format(new_friend.name), api)
                return
        page_no += 1
    tweet("I can't find any new friends.", api)
