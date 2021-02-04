from unittest import TestCase

from testfixtures import LogCapture

from utils import log_check

from guineabot.age_logging import configure_logging, logging
from guineabot.sayings import Sayings


class TestSayings(TestCase):

    def setUp(self) -> None:
        configure_logging()

    def test_default(self) -> None:
        with LogCapture(level=logging.INFO) as log_out:
            Sayings()
        self.assertTrue(log_out.records[0].msg.startswith('INITIALISE >> Loading sayings from:'))

    def test_no_file(self) -> None:
        with self.assertRaises(FileNotFoundError):
            Sayings('no_such_file.json')

    def test_file(self) -> None:
        with LogCapture(level=logging.INFO) as log_out:
            Sayings('./tests/test_sayings.json')
        log_check(log_out,
                  "INITIALISE >> Loading sayings from: tests/test_sayings.json")

    def test_random_saying(self) -> None:
        with LogCapture(level=logging.INFO) as log_out:
            sayings = Sayings('./tests/test_sayings.json')
        log_check(log_out,
                  "INITIALISE >> Loading sayings from: tests/test_sayings.json")
        saying = sayings.get_random_saying('TEST2')
        self.assertIn(saying, ["TEST2 SAYING1", "TEST2 SAYING2", "TEST2 SAYING3"])

    def test_random_photo_saying(self) -> None:
        with LogCapture(level=logging.INFO) as log_out:
            sayings = Sayings('./tests/test_sayings.json')
        log_check(log_out,
                  "INITIALISE >> Loading sayings from: tests/test_sayings.json")
        saying = sayings.get_random_photo_saying()
        self.assertIn(saying, ["PHOTO SAYING1", "PHOTO SAYING2", "PHOTO SAYING3"])
