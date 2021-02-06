import re

from typing import List, Optional

from environs import Env
from tweepy import API, Cursor, OAuthHandler, TweepError, User

from .age_logging import age_logger


class TwitterService:
    """
    Interface to define the function signatures for interacting with Twitter.
    """

    def tweet(self, message: str) -> None:
        """
        Tweet the supplied message.
        :param message: String to tweet
        :return: No meaningful return
        """
        pass    # pragma: no cover

    def tweet_with_photo(self, message: str, photo_path: str) -> None:
        """
        Tweet the supplied message and photo.
        :param message: String to tweet
        :param photo_path: Path to photo to tweet
        :return: No meaningful return
        """
        pass    # pragma: no cover

    def get_current_friends(self) -> List[int]:
        """
        Get a list of the current friends.
        :return: List of friend ids
        """
        pass    # pragma: no cover

    def find_new_friend(self, friends: List[int]) -> List[int]:
        """
        Find and follow a new friend who passes the friendship test.
        :param friends: Current list of friend ids
        :return: Updated list of friend ids
        """
        pass    # pragma: no cover

    def prune_friends(self, friends: List[int]) -> List[int]:
        """
        Remove friends who no longer pass the friendship test, unless they are following us, in which case mute them.
        :param friends: Current list of friend ids
        :return: Updated list of friend ids
        """
        pass    # pragma: no cover

    def unmute_all(self) -> None:
        """
        Maintenance function to remove all mutes from friends.
        :return: No meaningful return
        """
        pass    # pragma: no cover


def get_twitter_service(quiet: bool) -> TwitterService:
    """
    Factory to return a Twitter service instance.
    :param quiet: If true return a dummy version of the service
    :return: Returns a TwitterService
    """
    if quiet:
        return TwitterServiceQuiet()
    else:
        return TwitterServiceLive()


class TwitterServiceQuiet(TwitterService):
    """
    Quiet version of the TwitterService.
    Logs what the live service would do without actually invoking the Twitter API.
    """

    def __init__(self) -> None:
        age_logger.info("Quiet Mode is On, no Tweeting please!")

    def tweet(self, message: str) -> None:
        age_logger.info("Would have tweeted: {0}".format(message))

    def tweet_with_photo(self, message: str, photo_path: str) -> None:
        age_logger.info("Would have tweeted: {0} {1}".format(message, photo_path))

    def get_current_friends(self) -> List[int]:
        return []

    def find_new_friend(self, friends: List[int]) -> List[int]:
        age_logger.info("Would have looked for a new friend!")
        return []

    def prune_friends(self, friends: List[int]) -> List[int]:
        age_logger.info("Would have tried to prune friends!")
        return []

    def unmute_all(self) -> None:
        age_logger.info("Would have un-muted all muted friends!")


class TwitterServiceLive(TwitterService):
    """
    Live version of the TwitterService.
    Invokes the Twitter API using the Tweepy module.
    """

    def __init__(self) -> None:
        env = Env()
        env.read_env("guinea-bot.env")
        self.__consumer_key = self.__getenv(env, "TWITTER_CONSUMER_KEY")
        self.__consumer_secret = self.__getenv(env, "TWITTER_CONSUMER_SECRET")
        self.__access_token = self.__getenv(env, "TWITTER_ACCESS_TOKEN")
        self.__access_token_secret = self.__getenv(env, "TWITTER_ACCESS_TOKEN_SECRET")
        self.__api = self.__get_api()

    @staticmethod
    def __getenv(env: Env, env_var_name: str) -> str:
        env_var = env(env_var_name, False)
        if not env_var:
            raise SystemExit("Unable to connect to the Twitter API, access token '{0}' not found!".format(env_var_name))
        return env_var

    def __get_api(self) -> API:
        auth = OAuthHandler(self.__consumer_key, self.__consumer_secret)
        auth.set_access_token(self.__access_token, self.__access_token_secret)
        api = API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        if not api.verify_credentials():
            raise SystemExit("Unable to connect to the Twitter API, please check your access tokens.")
        return api

    def tweet(self, message: str) -> None:
        try:
            self.__api.update_status(message)
            age_logger.info("Tweeted: {0}".format(message))
        except TweepError as error:
            if error.api_code == 187:
                age_logger.warning("Duplicate tweet discarded!")
            else:
                age_logger.error("Error trying to tweet!", error)
                raise error

    def tweet_with_photo(self, message: str, photo_path: str) -> None:
        try:
            media = self.__api.media_upload(photo_path)
            self.__api.update_status(message, media_ids=[media.media_id])
            age_logger.info("Tweeted: {0} {1}".format(message, photo_path))
        except TweepError as error:
            if error.api_code == 187:
                age_logger.warning("Duplicate photo tweet discarded!")
            else:
                age_logger.error("Error trying to tweet with photo!", error)
                raise error

    def get_current_friends(self) -> List[int]:
        return self.__api.friends_ids()

    @staticmethod
    def __search_string(find: str, in_string: str) -> bool:
        return re.search(find, in_string, re.IGNORECASE) is not None

    @classmethod
    def __search(cls, string: str, flags: [str]) -> int:
        found = 0
        for flag in flags:
            if cls.__search_string(flag, string):
                found = found + 1
        return found

    @classmethod
    def __friendship_test(cls, new_friend: User) -> bool:
        description = new_friend.__getattribute__("description")
        red_flags = [r"anti.?vax"]
        if cls.__search(description, red_flags) > 0:
            return False
        key_term = r"guinea.?pig"
        green_flags = [key_term]
        return cls.__search_string(key_term, new_friend.__getattribute__("name")) or \
            cls.__search_string(key_term, new_friend.__getattribute__("screen_name")) or \
            cls.__search(description, green_flags) > 0

    def search_for_users(self, friends: List[int]) -> Optional[User]:
        page_no = 0
        while page_no < 100:
            page = self.__api.search_users("#guineapig", 20, page_no)
            for new_friend in page:
                if not new_friend.follow_request_sent and \
                        new_friend.id not in friends and \
                        self.__friendship_test(new_friend):
                    return new_friend
            page_no += 1
        return None

    def find_new_friend(self, friends: List[int]) -> List[int]:
        new_friend = self.search_for_users(friends)
        if new_friend:
            new_friend.follow()
            friends.append(new_friend.__getattribute__("id"))
            self.tweet("I've decided to follow {0}.".format(new_friend.__getattribute__("name")))
        else:
            self.tweet("I can't find any new friends.",)
        return friends

    def __examine_friendships(self, friends: List[User], my_id: int, muted: List[int]):
        for friend in friends:
            if not self.__friendship_test(friend):
                if my_id in friend.followers_ids():
                    friend_id = friend.__getattribute__("id")
                    if friend_id not in muted:
                        self.__api.create_mute(friend_id)
                        age_logger.info("Muted: {0}".format(friend))
                else:
                    friend.unfollow()
                    age_logger.info("Un-followed: {0}".format(friend))

    def prune_friends(self, friends: List[int]) -> List[int]:
        muted = self.__api.mutes_ids()
        my_id = self.__api.me().__getattribute__("id")
        # API call limited to 100 entries.
        for page in Cursor(self.__api.friends).pages():
            age_logger.info("Look for friends to prune...{0}".format(len(page)))
            self.__examine_friendships(page, my_id, muted)
        return self.get_current_friends()

    def unmute_all(self) -> None:
        muted = self.__api.mutes_ids()
        for mute in muted:
            self.__api.destroy_mute(mute)
