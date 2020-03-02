from .guineapig import GuineaPig
from .statemachine import State

from random import randint
from typing import List


SLEEPING = "SLEEPING"
EATING = "EATING"
DRINKING = "DRINKING"
WANDERING = "WANDERING"
THINKING = "THINKING"
AWAKE = "AWAKE"


class GuineaPigState(State):

    def __init__(self, state_name: str, changes: List[int]) -> None:
        self.__changes = changes
        super(GuineaPigState, self).__init__(state_name.upper())

    def transition(self, gp: GuineaPig) -> str:
        gp.update(self.get_name(), self.__changes)
        if gp.is_tired():
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
