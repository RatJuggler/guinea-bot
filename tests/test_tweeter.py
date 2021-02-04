from unittest import TestCase

from guineabot.tweeter import Tweeter
from unittest.mock import patch, MagicMock, Mock


class TestTweeter(TestCase):

    def setUp(self) -> None:
        pass

    def test_tweet(self) -> None:
        twitter_service_mock = Mock()
        tweeter = Tweeter(Mock(), Mock(), twitter_service_mock)
        tweeter.tweet("test")
        twitter_service_mock.tweet.assert_called_once()
        twitter_service_mock.tweet.assert_called_with("test")

    @patch("guineabot.tweeter.randint")
    def test_tweet_state(self,
                         randint_mock: MagicMock) -> None:
        randint_mock.return_value = 1
        sayings_mock = Mock()
        sayings_mock.get_random_saying.return_value = "saying"
        twitter_service_mock = Mock()
        tweeter = Tweeter(sayings_mock, Mock(), twitter_service_mock)
        tweeter.tweet_state("state")
        twitter_service_mock.tweet.assert_called_once()
        twitter_service_mock.tweet.assert_called_with("saying")

    @patch("guineabot.tweeter.randint")
    def test_tweet_state_with_photo(self,
                                    randint_mock: MagicMock) -> None:
        randint_mock.return_value = 11
        sayings_mock = Mock()
        sayings_mock.get_random_photo_saying.return_value = "saying"
        photos_mock = Mock()
        photos_mock.loaded.return_value = True
        photos_mock.get_path_to_random.return_value = "photo"
        twitter_service_mock = Mock()
        tweeter = Tweeter(sayings_mock, photos_mock, twitter_service_mock)
        tweeter.tweet_state("state")
        twitter_service_mock.tweet_with_photo.assert_called_once()
        twitter_service_mock.tweet_with_photo.assert_called_with("saying", "photo")
