from unittest import TestCase

from testfixtures import LogCapture

from tests.utils import log_check

from guineabot.age_logging import configure_logging, logging
from guineabot.photos import Photos


class TestPhotos(TestCase):

    def setUp(self) -> None:
        configure_logging()

    def test_no_photos(self) -> None:
        photos = Photos("")
        self.assertFalse(photos.loaded())

    def test_load_photos(self) -> None:
        with LogCapture(level=logging.INFO) as log_out:
            photos = Photos("./tests/photos")
        self.assertTrue(photos.loaded())
        log_check(log_out,
                  "INITIALISE >> Loading photos from: tests/photos")

    def test_random(self) -> None:
        with LogCapture(level=logging.INFO) as log_out:
            photos = Photos("./tests/photos")
        log_check(log_out,
                  "INITIALISE >> Loading photos from: tests/photos")
        photo = photos.get_path_to_random()
        self.assertIn(photo, ["tests/photos/photo1.jpg", "tests/photos/photo2.jpg", "tests/photos/photo3.jpg"])
