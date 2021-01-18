from unittest import TestCase

from guineabot.age_tracker import AgeTracker


class TestAgeTracker(TestCase):

    def setUp(self) -> None:
        pass

    def test_initial_str(self) -> None:
        at = AgeTracker(1, 1)
        self.assertEqual(at.__str__(), 'Age: 0 - 00:00')

    def test_single_interval(self) -> None:
        at = AgeTracker(99, 13)
        self.assertFalse(at.has_died())
        at.increase()
        self.assertFalse(at.has_died())
        self.assertEqual(at.__str__(), 'Age: 0 - 00:13')

    def test_multiple_intervals(self) -> None:
        at = AgeTracker(99, 22)
        for i in range(127):
            self.assertFalse(at.has_died())
            at.increase()
        self.assertFalse(at.has_died())
        self.assertEqual(at.__str__(), 'Age: 1 - 22:34')

    def test_end_interval(self) -> None:
        at = AgeTracker(2, 30)
        duration = 60 // 30 * 24 * 2
        for i in range(duration):
            self.assertFalse(at.has_died())
            at.increase()
        self.assertTrue(at.has_died())
        self.assertEqual(at.__str__(), 'Age: 2 - 00:00')
