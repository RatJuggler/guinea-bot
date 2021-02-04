from unittest import TestCase
from testfixtures import LogCapture
from unittest.mock import patch, MagicMock

from utils import log_check

from guineabot.age_logging import configure_logging, logging
from guineabot.twitter_api import TwitterServiceQuiet, TwitterServiceLive


class TestTwitterServiceQuiet(TestCase):

    def setUp(self) -> None:
        configure_logging()

    def test_tweet(self) -> None:
        with LogCapture(level=logging.INFO) as log_out:
            TwitterServiceQuiet().tweet("test")
        log_check(log_out,
                  "INITIALISE >> Quiet Mode is On, no Tweeting please!",
                  "INITIALISE >> Would have tweeted: test")

    def test_tweet_with_photo(self) -> None:
        with LogCapture(level=logging.INFO) as log_out:
            TwitterServiceQuiet().tweet_with_photo("test", "photo")
        log_check(log_out,
                  "INITIALISE >> Quiet Mode is On, no Tweeting please!",
                  "INITIALISE >> Would have tweeted: test photo")

    def test_get_current_friends(self) -> None:
        with LogCapture(level=logging.INFO) as log_out:
            self.assertEqual([], TwitterServiceQuiet().get_current_friends())
        log_check(log_out,
                  "INITIALISE >> Quiet Mode is On, no Tweeting please!")

    def test_find_new_friend(self) -> None:
        with LogCapture(level=logging.INFO) as log_out:
            self.assertEqual([], TwitterServiceQuiet().find_new_friend([]))
        log_check(log_out,
                  "INITIALISE >> Quiet Mode is On, no Tweeting please!",
                  "INITIALISE >> Would have looked for a new friend!")

    def test_prune_friends(self) -> None:
        with LogCapture(level=logging.INFO) as log_out:
            self.assertEqual([], TwitterServiceQuiet().prune_friends([]))
        log_check(log_out,
                  "INITIALISE >> Quiet Mode is On, no Tweeting please!",
                  "INITIALISE >> Would have tried to prune friends!")

    def test_unmute_all(self) -> None:
        with LogCapture(level=logging.INFO) as log_out:
            TwitterServiceQuiet().unmute_all()
        log_check(log_out,
                  "INITIALISE >> Quiet Mode is On, no Tweeting please!",
                  "INITIALISE >> Would have un-muted all muted friends!")


@patch("guineabot.twitter_api.OAuthHandler")
@patch("guineabot.twitter_api.API")
class TestTwitterServiceLive(TestCase):

    def setUp(self) -> None:
        configure_logging()

    def test_tweet(self,
                   tweepy_api_mock: MagicMock,
                   tweepy_oauthhandler_mock: MagicMock) -> None:
        with LogCapture(level=logging.INFO) as log_out:
            TwitterServiceLive().tweet("test")
        log_check(log_out,
                  "INITIALISE >> Tweeted: test")
        tweepy_oauthhandler_mock.return_value.set_access_token.assert_called_once()
        tweepy_api_mock.return_value.update_status.assert_called_with("test")

    def test_tweet_with_photo(self,
                              tweepy_api_mock: MagicMock,
                              tweepy_oauthhandler_mock: MagicMock) -> None:
        with LogCapture(level=logging.INFO) as log_out:
            TwitterServiceLive().tweet_with_photo("test", "photo")
        log_check(log_out,
                  "INITIALISE >> Tweeted: test photo")
        tweepy_oauthhandler_mock.return_value.set_access_token.assert_called_once()
        tweepy_api_mock.return_value.media_upload.assert_called_with("photo")
        tweepy_api_mock.return_value.update_status.assert_called_with(
            "test", media_ids=[tweepy_api_mock.return_value.media_upload.return_value.media_id])

    def test_get_current_friends(self,
                                 tweepy_api_mock: MagicMock,
                                 tweepy_oauthhandler_mock: MagicMock) -> None:
        TwitterServiceLive().get_current_friends()
        tweepy_oauthhandler_mock.return_value.set_access_token.assert_called_once()
        tweepy_api_mock.return_value.friends_ids.assert_called_once()
