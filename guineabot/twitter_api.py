import os
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


def tweet(message):
    twitter_api = create_twitter_api()
    try:
        twitter_api.update_status(message)
    except tweepy.TweepError as error:
        if error.api_code == 187:
            print('Duplicate tweet discarded.')
        else:
            raise error
