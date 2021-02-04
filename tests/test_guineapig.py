import os

from unittest import TestCase
from unittest.mock import Mock

from guineabot.guineapig import GuineaPig, build_save_filename


class TestGuineaPig(TestCase):

    def setUp(self) -> None:
        self.__name = "TestGP"
        self.__save_file = build_save_filename(os.environ.get('HOME', ''), self.__name)

    def build_guinea_pig(self, lifespan: int = 9) -> GuineaPig:
        return GuineaPig(self.__name, self.__save_file, lifespan, 0, "SLEEPING", 20, 10, 10, Mock())

    def check_state(self, gp: GuineaPig, lifespan: int, age: int, state: str, tired: int, hunger: int, thirst: int) -> None:
        self.assertEqual("GuineaPig:(Name: {0}, Save File: {1}, Lifespan: {2} days, Current Age: {3} mins, State: {4}, "
                         "Tired: {5}, Hunger: {6}, Thirst: {7})"
                         .format(self.__name, self.__save_file, lifespan, age, state, tired, hunger, thirst), gp.__str__())

    def test_initial_str(self) -> None:
        gp = self.build_guinea_pig()
        self.check_state(gp, 9, 0, "SLEEPING", 20, 10, 10)

    def test_single_update(self) -> None:
        gp = self.build_guinea_pig()
        self.assertFalse(gp.has_died())
        gp.update("TEST_STATE", [1, 2, 3], 1)
        self.assertFalse(gp.has_died())
        self.check_state(gp, 9, 1, "TEST_STATE", 21, 12, 13)

    def test_multiple_updates(self) -> None:
        gp = self.build_guinea_pig()
        for i in range(27):
            self.assertFalse(gp.has_died())
            gp.update("TEST_STATE", [1, 2, 3], 1)
        self.assertFalse(gp.has_died())
        self.check_state(gp, 9, 27, "TEST_STATE", 47, 64, 91)

    def test_can_die(self) -> None:
        lifespan = 4
        gp = self.build_guinea_pig(lifespan)
        for i in range(lifespan * 24 * 60):
            self.assertFalse(gp.has_died())
            gp.update("TEST_STATE", [0, 0, 0], 1)
        self.assertTrue(gp.has_died())
        self.check_state(gp, lifespan, 5760, "TEST_STATE", 20, 10, 10)
