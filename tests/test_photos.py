from unittest import TestCase

from guineabot.photos import Photos


class TestPhotos(TestCase):

    def setUp(self) -> None:
        pass

    def test_no_photos(self) -> None:
        photos = Photos("")
        self.assertFalse(photos.loaded())

    def test_load_photos(self) -> None:
        photos = Photos("tests/photos")
        self.assertTrue(photos.loaded())

    def test_random(self) -> None:
        photos = Photos("tests/photos")
        photo = photos.get_path_to_random()
        self.assertIn(photo, ["tests/photos/photo1.jpg", "tests/photos/photo2.jpg", "tests/photos/photo3.jpg"])
