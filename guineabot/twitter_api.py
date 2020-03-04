import os
import re

from typing import List

import tweepy
from tweepy import API

from .smt_logging import smt_logger


class TwitterService:

    def tweet(self, message: str) -> None:
        pass

    def tweet_with_photo(self, message: str, photo_path: str) -> None:
        pass

    def get_current_friends(self) -> List[int]:
        pass

    def find_new_friend(self, friends: List[int]) -> List[int]:
        pass

    def prune_friends(self, friends: List[int]) -> List[int]:
        pass


def get_twitter_service(quiet: bool) -> TwitterService:
    if quiet:
        return TwitterServiceQuiet()
    else:
        return TwitterServiceLive()


class TwitterServiceQuiet(TwitterService):

    def __init__(self) -> None:
        smt_logger.info("Quiet Mode On!")

    def tweet(self, message: str) -> None:
        smt_logger.info("Would have tweeted: {0}".format(message))

    def tweet_with_photo(self, message: str, photo_path: str) -> None:
        smt_logger.info("Would have tweeted: {0} {1}".format(message, photo_path))

    def get_current_friends(self) -> List[int]:
        return []

    def find_new_friend(self, friends: List[int]) -> List[int]:
        smt_logger.info("Would have looked for a new friend!")
        return []

    def prune_friends(self, friends: List[int]) -> List[int]:
        smt_logger.info("Would have tried to pruned friends!")
        return []


class TwitterServiceLive(TwitterService):

    def __init__(self) -> None:
        self.__consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
        self.__consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
        self.__access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        self.__access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
        self.__api = self.__get_api()

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

    def tweet(self, message: str) -> None:
        try:
            self.__api.update_status(message)
            smt_logger.info("Tweeted: {0}".format(message))
        except tweepy.TweepError as error:
            if error.api_code == 187:
                smt_logger.warning("Duplicate tweet discarded!")
            else:
                smt_logger.error("Error trying to tweet!", error)
                raise error

    def tweet_with_photo(self, message: str, photo_path: str) -> None:
        try:
            media = self.__api.media_upload(photo_path)
            self.__api.update_status(message, media_ids=[media.media_id])
            smt_logger.info("Tweeted: {0} {1}".format(message, photo_path))
        except tweepy.TweepError as error:
            if error.api_code == 187:
                smt_logger.warning("Duplicate photo tweet discarded!")
            else:
                smt_logger.error("Error trying to tweet with photo!", error)
                raise error

    def get_current_friends(self) -> List[int]:
        return self.__api.friends_ids()

    @staticmethod
    def __good_name(name: str) -> bool:
        return re.search(r"guinea\s*pig", name, re.IGNORECASE) is not None

    @classmethod
    def __friendship_test(cls, name: str, screen_name: str) -> bool:
        return cls.__good_name(name) or cls.__good_name(screen_name)

    def find_new_friend(self, friends: List[int]) -> List[int]:
        page_no = 0
        while page_no < 100:
            page = self.__api.search_users("guinea pig", 20, page_no)
            for new_friend in page:
                if new_friend.id not in friends and self.__friendship_test(new_friend.name, new_friend.screen_name):
                    new_friend.follow()
                    friends.append(new_friend.id)
                    self.tweet("I've decided to follow {0}.".format(new_friend.name))
                    return friends
            page_no += 1
        self.tweet("I can't find any new friends.",)
        return friends

    def prune_friends(self, friends: List[int]) -> List[int]:
        for friendship in self.__api.lookup_friendships(friends):
            if not self.__friendship_test(friendship.name, friendship.screen_name):
                if friendship.is_followed_by:
                    self.__api.create_mute(friendship.id)
                    smt_logger.info("Muted: {0} - {1}".format(friendship.name, friendship.screen_name))
                else:
                    self.__api.destroy_friendship(friendship.id)
                    smt_logger.info("Un-followed: {0} - {1}".format(friendship.name, friendship.screen_name))
        return self.get_current_friends()
