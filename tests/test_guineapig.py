from unittest import TestCase
from unittest.mock import Mock

from guineabot.guineapig import GuineaPig


class TestGuineaPig(TestCase):

    def setUp(self) -> None:
        pass

    def test_initial_str(self) -> None:
        gp = GuineaPig("TestGP", 9, 0, "SLEEPING", 20, 10, 10, Mock())
        self.assertEqual("GuineaPig:(Name: TestGP, Lifespan: 9 days, Current Age: 0 mins, State: SLEEPING, "
                         "Tired: 20, Hunger: 10, Thirst: 10)", gp.__str__())

    def test_single_update(self) -> None:
        gp = GuineaPig("TestGP", 9, 0, "SLEEPING", 20, 10, 10, Mock())
        self.assertFalse(gp.has_died())
        gp.update("TEST_STATE", [1, 2, 3], 1)
        self.assertFalse(gp.has_died())
        self.assertEqual("GuineaPig:(Name: TestGP, Lifespan: 9 days, Current Age: 1 mins, State: TEST_STATE, "
                         "Tired: 21, Hunger: 12, Thirst: 13)", gp.__str__())

    def test_multiple_updates(self) -> None:
        gp = GuineaPig("TestGP", 9, 0, "SLEEPING", 20, 10, 10, Mock())
        for i in range(27):
            self.assertFalse(gp.has_died())
            gp.update("TEST_STATE", [1, 2, 3], 1)
        self.assertFalse(gp.has_died())
        self.assertEqual("GuineaPig:(Name: TestGP, Lifespan: 9 days, Current Age: 27 mins, State: TEST_STATE, "
                         "Tired: 47, Hunger: 64, Thirst: 91)", gp.__str__())

    def test_can_die(self) -> None:
        lifespan = 4
        gp = GuineaPig("TestGP", lifespan, 0, "SLEEPING", 20, 10, 10, Mock())
        for i in range(lifespan * 24 * 60):
            self.assertFalse(gp.has_died())
            gp.update("TEST_STATE", [0, 0, 0], 1)
        self.assertTrue(gp.has_died())
        self.assertEqual("GuineaPig:(Name: TestGP, Lifespan: 4 days, Current Age: 5760 mins, State: TEST_STATE, "
                         "Tired: 20, Hunger: 10, Thirst: 10)", gp.__str__())
