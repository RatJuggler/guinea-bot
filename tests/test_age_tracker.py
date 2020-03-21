from unittest import TestCase

from age_tracker import AgeTracker


class TestAgeTracker(TestCase):

    def setUp(self) -> None:
        pass

    def test_initial_str(self) -> None:
        at = AgeTracker(1, 1, True)
        self.assertEqual(at.__str__(), 'Age: 0 - 00:00')

    def test_single_interval(self) -> None:
        at = AgeTracker(99, 13, True)
        self.assertTrue(at.increase())
        self.assertEqual(at.__str__(), 'Age: 0 - 00:13')

    def test_multiple_intervals(self) -> None:
        at = AgeTracker(99, 22, True)
        for i in range(127):
            self.assertTrue(at.increase())
        self.assertEqual(at.__str__(), 'Age: 1 - 22:34')

    def test_end_interval(self) -> None:
        at = AgeTracker(2, 30, True)
        duration = 60 // 30 * 24 * 2
        for i in range(duration - 1):
            self.assertTrue(at.increase())
        self.assertFalse(at.increase())
        self.assertEqual(at.__str__(), 'Age: 2 - 00:00')
