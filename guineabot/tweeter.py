from random import randint

from .photos import Photos
from .sayings import Sayings
from .twitter_api import TwitterService, get_twitter_service


class Tweeter:
    """
    Everything a guinea pig needs to tweet.
    """

    def __init__(self, sayings: Sayings, photos: Photos, tweeter: TwitterService) -> None:
        """
        Initialise the guinea pig process.
        :param sayings: Supplies sayings for tweeting
        :param photos: Supplies photos for tweeting
        :param tweeter: Tweeting service to use
        """
        self.__sayings = sayings
        self.__photos = photos
        self.__tweeter = tweeter
        self.__friends = self.__tweeter.get_current_friends()

    def tweet_state(self, state: str) -> None:
        """
        Tweet, tweet with a photo or find new friends.
        This is limited using random checks to prevent the timeline being flooded and from accumulating friends too quickly.
        :param state: To tweet for
        :return: No meaningful return
        """
        chance = randint(1, 80)
        if chance <= 10:
            self.__tweeter.tweet(self.__sayings.get_random_saying(state))
        elif chance == 11:
            if self.__photos.loaded():
                self.__tweeter.tweet_with_photo(self.__sayings.get_random_photo_saying(),
                                                self.__photos.get_path_to_random())
        # elif chance == 12:
        #     self.__friends = self.__tweeter.find_new_friend(self.__friends)


def create_tweeter(path_to_photos: str, quiet: bool) -> Tweeter:
    """
    Create a tweeter service instance.
    :param path_to_photos: Path to folder of photos for tweeting
    :param quiet: Run without invoking the Twitter API
    :return: A new instance of the tweeter service
    """
    return Tweeter(Sayings(), Photos(path_to_photos), get_twitter_service(quiet))
