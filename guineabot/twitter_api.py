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
    except Exception as e:
        print("Error creating Twitter API: {0}".format(e))
        raise e
    return api


def tweet(message, api=None):
    if not api:
        api = create_twitter_api()
    try:
        api.update_status(message)
    except tweepy.TweepError as error:
        if error.api_code == 187:
            print("Duplicate tweet discarded!")
        else:
            raise error


def get_current_friends():
    return create_twitter_api().friends_ids()


def good_name(name):
    return re.search(r"guinea\s*pig", name, re.IGNORECASE)


def find_new_friend(friends):
    page_no = 0
    api = create_twitter_api()
    while page_no < 100:
        page = api.search_users("guinea pig", 20, page_no)
        for new_friend in page:
            if new_friend.id not in friends and good_name(new_friend.name) or good_name(new_friend.screen_name):
                new_friend.follow()
                friends.append(new_friend.id)
                tweet("I've decided to follow {0}.".format(new_friend.name), api)
        page_no += 1
    tweet("I can't find any new friends.", api)
