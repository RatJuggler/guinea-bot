from random import randint
from typing import List

from .guineapig import GuineaPig
from .statemachine import StateMachine, State

# Current guinea pig states.
SLEEPING = "SLEEPING"
EATING = "EATING"
DRINKING = "DRINKING"
WANDERING = "WANDERING"
THINKING = "THINKING"
AWAKE = "AWAKE"
# The end state.
END = "END"


class GuineaPigState(State):
    """
    The common class which defines each state of the guinea pig.
    """

    def __init__(self, state_name: str, changes: List[int]) -> None:
        """
        Initialise a guinea pig state instance.
        :param state_name: The name of the state
        :param changes: The guinea pig attributes the state affects
        """
        self.__changes = changes
        super(GuineaPigState, self).__init__(state_name.upper())

    @staticmethod
    def __determine_new_state(gp: GuineaPig) -> str:
        """
        Determine what guinea pig will do next.
        :return: The name of the next state (not necessarily different to the current state)
        """
        if gp.has_died():
            new_state = END
        elif gp.is_tired():
            new_state = SLEEPING
        elif gp.is_hungry():
            new_state = EATING
        elif gp.is_thirsty():
            new_state = DRINKING
        elif randint(1, 10) > 5:
            new_state = WANDERING
        elif randint(1, 10) > 8:
            new_state = THINKING
        else:
            new_state = AWAKE
        return new_state

    def transition(self, gp: GuineaPig) -> str:
        """
        Update the attributes and then determine the next state for the given guinea pig.
        :param gp: A guinea pig instance
        :return: The name of the next state (not necessarily different to the current state)
        """
        gp.update(self.get_name(), self.__changes)
        return self.__determine_new_state(gp)


def build_guinea_pig_machine(interval: int, accelerated: bool) -> StateMachine:
    """
    Initialise the state machine.
    :param interval: The time interval between each tick of the state machine clock (in minutes)
    :param accelerated: Don't wait for the time interval
    :return: StateMachine instance with states configured
    """
    sm = StateMachine(SLEEPING, END, interval, accelerated)
    sm.add_state(GuineaPigState(SLEEPING, [-20, 3, 1]))
    sm.add_state(GuineaPigState(AWAKE, [5, 5, 2]))
    sm.add_state(GuineaPigState(THINKING, [1, 3, 1]))
    sm.add_state(GuineaPigState(EATING, [5, -10, 4]))
    sm.add_state(GuineaPigState(DRINKING, [5, 5, -80]))
    sm.add_state(GuineaPigState(WANDERING, [10, 10, 5]))
    return sm
