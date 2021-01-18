from unittest import TestCase
from unittest.mock import Mock

from guineabot.guineapig import GuineaPig


class TestGuineaPig(TestCase):

    def setUp(self) -> None:
        pass

    def test_initial_str(self) -> None:
        gp = GuineaPig("Test", 99, 0, "SLEEPING", 20, 10, 10, Mock())
        self.assertEqual(gp.__str__(), "GuineaPig:(Name: Test, State: SLEEPING, Hunger: 10, Thirst: 10, Tired: 20)")

    def test_single_update(self) -> None:
        gp = GuineaPig("Test", 99, 0, "SLEEPING", 20, 10, 10, Mock())
        self.assertFalse(gp.has_died())
        gp.update("TEST", [1, 2, 3], 1)
        self.assertFalse(gp.has_died())
        self.assertEqual(gp.__str__(), "GuineaPig:(Name: Test, State: TEST, Hunger: 12, Thirst: 13, Tired: 21)")

    def test_multiple_updates(self) -> None:
        gp = GuineaPig("Test", 99, 0, "SLEEPING", 20, 10, 10, Mock())
        for i in range(127):
            self.assertFalse(gp.has_died())
            gp.update("TEST", [0, 0, 0], 1)
        self.assertFalse(gp.has_died())
        self.assertEqual(gp.__str__(), "GuineaPig:(Name: Test, State: TEST, Hunger: 10, Thirst: 10, Tired: 20)")

    def test_end_interval(self) -> None:
        gp = GuineaPig("Test", 9, 0, "SLEEPING", 20, 10, 10, Mock())
        duration = 9 * 24 * 60
        for i in range(duration):
            self.assertFalse(gp.has_died())
            gp.update("TEST", [0, 0, 0], 1)
        self.assertTrue(gp.has_died())
        self.assertEqual(gp.__str__(), "GuineaPig:(Name: Test, State: TEST, Hunger: 10, Thirst: 10, Tired: 20)")
