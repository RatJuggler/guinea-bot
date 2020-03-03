import os
import re

from typing import List

import tweepy
from tweepy import API

from .smt_logging import smt_logger


class TwitterService:

    def tweet(self, message: str, api: API = None) -> None:
        pass

    def tweet_with_photo(self, message: str, photo_path: str, api: API = None) -> None:
        pass

    def get_current_friends(self, api: API = None) -> List[int]:
        pass

    def find_new_friend(self, friends: List[int], api: API = None) -> None:
        pass

    def prune_friends(self):
        pass


def get_twitter_service(quiet: bool) -> TwitterService:
    if quiet:
        return TwitterServiceQuiet()
    else:
        return TwitterServiceLive()


class TwitterServiceQuiet(TwitterService):

    def __init__(self) -> None:
        smt_logger.info("Quiet Mode On!")

    def tweet(self, message: str, api: API = None) -> None:
        smt_logger.info("Would have tweeted: {0}".format(message))

    def tweet_with_photo(self, message: str, photo_path: str, api: API = None) -> None:
        smt_logger.info("Would have tweeted: {0} {1}".format(message, photo_path))

    def get_current_friends(self, api: API = None) -> List[int]:
        return []

    def find_new_friend(self, friends: List[int], api: API = None) -> None:
        smt_logger.info("Would have looked for a new friend!")

    def prune_friends(self):
        smt_logger.info("Would have pruned friends!")


class TwitterServiceLive(TwitterService):

    def __init__(self) -> None:
        self.__consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
        self.__consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
        self.__access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        self.__access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

    def __get_api(self) -> API:
        auth = tweepy.OAuthHandler(self.__consumer_key, self.__consumer_secret)
        auth.set_access_token(self.__access_token, self.__access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        try:
            api.verify_credentials()
        except Exception as error:
            smt_logger.error("Error creating Twitter API!", error)
            raise error
        return api

    def tweet(self, message: str, api: API = None) -> None:
        if not api:
            api = self.__get_api()
        try:
            api.update_status(message)
            smt_logger.info("Tweeted: {0}".format(message))
        except tweepy.TweepError as error:
            if error.api_code == 187:
                smt_logger.warning("Duplicate tweet discarded!")
            else:
                smt_logger.error("Error trying to tweet!", error)
                raise error

    def tweet_with_photo(self, message: str, photo_path: str, api: API = None) -> None:
        if not api:
            api = self.__get_api()
        try:
            media = api.media_upload(photo_path)
            api.update_status(message, media_ids=[media.media_id])
            smt_logger.info("Tweeted: {0} {1}".format(message, photo_path))
        except tweepy.TweepError as error:
            if error.api_code == 187:
                smt_logger.warning("Duplicate photo tweet discarded!")
            else:
                smt_logger.error("Error trying to tweet with photo!", error)
                raise error

    def get_current_friends(self, api: API = None) -> List[int]:
        if not api:
            api = self.__get_api()
        return api.friends_ids()

    @staticmethod
    def __good_name(name: str) -> bool:
        return re.search(r"guinea\s*pig", name, re.IGNORECASE) is not None

    def find_new_friend(self, friends: List[int], api: API = None) -> List[int]:
        page_no = 0
        if not api:
            api = self.__get_api()
        if not friends or len(friends) == 0:
            smt_logger.warning("Expected more friends: {0}".format(friends))
            friends = self.get_current_friends(api)
        while page_no < 100:
            page = api.search_users("guinea pig", 20, page_no)
            for new_friend in page:
                if new_friend.id not in friends and (self.__good_name(new_friend.name) or self.__good_name(new_friend.screen_name)):
                    new_friend.follow()
                    friends.append(new_friend.id)
                    self.tweet("I've decided to follow {0}.".format(new_friend.name), api)
                    return friends
            page_no += 1
        self.tweet("I can't find any new friends.", api)
        return friends

    def prune_friends(self):
        pass
