from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from .age import Age
from .age_logging import age_logger

T = TypeVar('T')


class State(ABC):
    """
    States are used to configure the StateMachine.
    """

    def __init__(self, name: str) -> None:
        """
        Initialise a State instance.
        :param name: The state name
        """
        self.__name = name
        super().__init__()

    def get_name(self) -> str:
        """
        The name of the state.
        :return: The state name
        """
        return self.__name

    @abstractmethod
    def transition(self, data: Generic[T]) -> str:
        """
        A transition to the next state.
        :param data: Object which informs the transition to the next state.
        :return: The name of the next state (not necessarily different to the current state)
        """
        raise NotImplementedError


class StateMachine:
    """
    A simple state machine driven by state transitions from the State interface.
    """

    def __init__(self, end_state_name: str) -> None:
        """
        Initialise a StateMachine instance.
        :param end_state_name: Termination state
        """
        self.__end_state_name = end_state_name
        self.__states = {}
        self.__counts = {}

    def add_state(self, new_state: State) -> None:
        """
        Add a new state to this machine instance.
        :param new_state: State to add
        :return: No meaningful return
        """
        self.__states[new_state.get_name()] = new_state
        self.__counts[new_state.get_name()] = 0

    def run(self, start_state_name: str, data: Generic[T]) -> None:
        """
        Run the state machine.
        :param start_state_name: Initial state
        :param data: Object which informs the state transition on the next state.
        :return: No meaningful return
        """
        new_state_name = start_state_name
        while new_state_name != self.__end_state_name:
            age_logger.debug("{0}".format(str(data)))
            state = self.__states[new_state_name]
            self.__counts[new_state_name] += 1
            new_state_name = state.transition(data)

    def stats(self, age: Age) -> None:
        """
        Log stats on time spent in each state.
        :param age: Age tracker to generate stats from
        :return: No meaningful return
        """
        age_logger.set_age('COMPLETED')
        age_logger.info("Dumping stats...\n{:>96}".format("State     : Time spent in state (% and daily avg.)"))
        for state in self.__counts:
            percentage, average = age.stats(self.__counts[state])
            age_logger.info("{0:9} : {1:04.2f}% - {2}".format(state, percentage, average))
