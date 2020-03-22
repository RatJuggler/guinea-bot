from unittest import TestCase

from guineabot.sayings import Sayings


class TestSayings(TestCase):

    def setUp(self) -> None:
        pass

    def test_default(self) -> None:
        Sayings()

    def test_no_file(self) -> None:
        with self.assertRaises(FileNotFoundError):
            Sayings('no_such_file.json')

    def test_file(self) -> None:
        Sayings('./tests/test_sayings.json')

    def test_random_saying(self) -> None:
        sayings = Sayings('./tests/test_sayings.json')
        saying = sayings.get_random_saying('TEST2')
        self.assertIn(saying, ["TEST2 SAYING1", "TEST2 SAYING2", "TEST2 SAYING3"])
