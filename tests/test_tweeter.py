from unittest import TestCase

from guineabot.tweeter import Tweeter
from unittest.mock import Mock


class TestTweeter(TestCase):

    def setUp(self) -> None:
        pass

    def test_tweet(self) -> None:
        twitter_service_mock = Mock()
        tweeter = Tweeter(Mock(), Mock(), twitter_service_mock)
        tweeter.tweet("test")
        twitter_service_mock.tweet.assert_called_with("test")
