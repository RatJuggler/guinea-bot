from unittest import TestCase
from unittest.mock import Mock

from guineabot.guineapig import GuineaPig
from guineabot.guineapig_states import GuineaPigState


class TestGuineaPigState(TestCase):

    def setUp(self) -> None:
        pass

    def test_state_transition(self) -> None:
        gp = GuineaPig("TestGP", 9, 0, "SLEEPING", 80, 10, 10, Mock())
        gps = GuineaPigState("TEST_STATE", [1, 2, 3])
        self.assertEqual("SLEEPING", gps.transition(1, gp))
        self.assertEqual("GuineaPig:(Name: TestGP, Lifespan: 9 days, Current Age: 1 mins, State: TEST_STATE, "
                         "Tired: 81, Hunger: 12, Thirst: 13)", gp.__str__())
