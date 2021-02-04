from unittest import TestCase
from testfixtures import LogCapture

from guineabot.age_logging import configure_logging
from guineabot.twitter_api import TwitterServiceQuiet

import guineabot.age_logging as al


def _log_check(log_out: LogCapture, *expects: str) -> None:
    root = "root"
    log_level = al.logging.getLevelName(al.logging.INFO)
    for expected in expects:
        log_out.check_present((root, log_level, expected))


class TestTwitterServiceQuiet(TestCase):

    def setUp(self) -> None:
        configure_logging()

    def test_tweet(self) -> None:
        with LogCapture(level=al.logging.INFO) as log_out:
            TwitterServiceQuiet().tweet("test")
        _log_check(log_out,
                   "INITIALISE >> Quiet Mode is On, no Tweeting please!",
                   "INITIALISE >> Would have tweeted: test")

    def test_tweet_with_photo(self) -> None:
        with LogCapture(level=al.logging.INFO) as log_out:
            TwitterServiceQuiet().tweet_with_photo("test", "photo")
        _log_check(log_out,
                   "INITIALISE >> Quiet Mode is On, no Tweeting please!",
                   "INITIALISE >> Would have tweeted: test photo")

    def test_get_current_friends(self) -> None:
        with LogCapture(level=al.logging.INFO) as log_out:
            self.assertEqual([], TwitterServiceQuiet().get_current_friends())
        _log_check(log_out,
                   "INITIALISE >> Quiet Mode is On, no Tweeting please!")

    def test_find_new_friend(self) -> None:
        with LogCapture(level=al.logging.INFO) as log_out:
            self.assertEqual([], TwitterServiceQuiet().find_new_friend([]))
        _log_check(log_out,
                   "INITIALISE >> Quiet Mode is On, no Tweeting please!",
                   "INITIALISE >> Would have looked for a new friend!")

    def test_prune_friends(self) -> None:
        with LogCapture(level=al.logging.INFO) as log_out:
            self.assertEqual([], TwitterServiceQuiet().prune_friends([]))
        _log_check(log_out,
                   "INITIALISE >> Quiet Mode is On, no Tweeting please!",
                   "INITIALISE >> Would have tried to prune friends!")

    def test_unmute_all(self) -> None:
        with LogCapture(level=al.logging.INFO) as log_out:
            TwitterServiceQuiet().unmute_all()
        _log_check(log_out,
                   "INITIALISE >> Quiet Mode is On, no Tweeting please!",
                   "INITIALISE >> Would have un-muted all muted friends!")
