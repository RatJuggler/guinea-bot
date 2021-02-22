import os

from unittest import TestCase
from unittest.mock import Mock

from guineabot.guineapig import GuineaPig, build_save_filename
from guineabot.guineapig_states import GuineaPigState


class TestGuineaPigState(TestCase):

    def setUp(self) -> None:
        self.__name = "TestGP"
        self.__save_file = build_save_filename(os.environ.get('HOME', ''), self.__name)

    def test_state_transition(self) -> None:
        gp = GuineaPig(self.__name, self.__save_file, 9, 0, "SLEEPING", 80, 10, 10, Mock(), None)
        gps = GuineaPigState("TEST_STATE", [1, 2, 3])
        self.assertEqual("SLEEPING", gps.transition(1, gp))
        self.assertEqual("GuineaPig:(Name: {0}, Save File: {1}, Lifespan: 9 days, Current Age: 1 mins, State: TEST_STATE, "
                         "Tired: 81, Hunger: 12, Thirst: 13)".format(self.__name, self.__save_file), gp.__str__())
