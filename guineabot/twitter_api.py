import logging
import os
import re

from typing import List

import tweepy
from tweepy import API


class TwitterService:

    def __init__(self, quiet: bool) -> None:
        self.quiet = quiet
        self.consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
        self.consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
        self.access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        self.access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
        if self.quiet:
            logging.info("Quiet Mode On!")

    def __get_api(self) -> API:
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        try:
            api.verify_credentials()
        except Exception as error:
            logging.error("Error creating Twitter API!", error)
            raise error
        return api

    def tweet(self, message: str, api: API = None) -> None:
        if self.quiet:
            logging.info("Would have tweeted: {0}".format(message))
            return
        if not api:
            api = self.__get_api()
        try:
            api.update_status(message)
            logging.info("Tweeted: {0}".format(message))
        except tweepy.TweepError as error:
            if error.api_code == 187:
                logging.warning("Duplicate tweet discarded!")
            else:
                logging.error("Error trying to tweet!", error)
                raise error

    def tweet_with_photo(self, message: str, photo_path: str, api: API = None) -> None:
        if self.quiet:
            logging.info("Would have tweeted: {0} {1}".format(message, photo_path))
            return
        if not api:
            api = self.__get_api()
        try:
            media = api.media_upload(photo_path)
            api.update_status(message, media_ids=[media.media_id])
            logging.info("Tweeted: {0} {1}".format(message, photo_path))
        except tweepy.TweepError as error:
            if error.api_code == 187:
                logging.warning("Duplicate photo tweet discarded!")
            else:
                logging.error("Error trying to tweet with photo!", error)
                raise error

    def get_current_friends(self, api: API = None) -> List[int]:
        if self.quiet:
            return []
        if not api:
            api = self.__get_api()
        return api.friends_ids()

    @staticmethod
    def __good_name(name: str) -> bool:
        return re.search(r"guinea\s*pig", name, re.IGNORECASE) is not None

    def find_new_friend(self, friends: List[int], api: API = None) -> None:
        if self.quiet:
            logging.info("Would have looked for a new friend!")
            return
        page_no = 0
        if not api:
            api = self.__get_api()
        if not friends or len(friends) == 0:
            logging.warning("Expected more friends: {0}".format(friends))
            friends = self.get_current_friends(api)
        while page_no < 100:
            page = api.search_users("guinea pig", 20, page_no)
            for new_friend in page:
                if new_friend.id not in friends and (self.__good_name(new_friend.name) or self.__good_name(new_friend.screen_name)):
                    new_friend.follow()
                    friends.append(new_friend.id)
                    self.tweet("I've decided to follow {0}.".format(new_friend.name), api)
                    return
            page_no += 1
        self.tweet("I can't find any new friends.", api)
