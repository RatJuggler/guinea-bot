from abc import ABC, abstractmethod
from time import sleep
from typing import Generic, TypeVar

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
    def transition(self, duration: int, data: Generic[T]) -> str:
        """
        A transition to the next state.
        :param duration: How long the new state will last (in minutes)
        :param data: Object which informs the transition to the next state.
        :return: The name of the next state (not necessarily different to the current state)
        """
        raise NotImplementedError


class StateMachine:
    """
    A simple state machine driven by state transitions from the State interface at fixed intervals.
    """

    def __init__(self, start_state_name: str, end_state_name: str, interval: int, accelerated: bool) -> None:
        """
        Initialise a StateMachine instance.
        :param start_state_name: Initial state
        :param end_state_name: Termination state
        :param interval: The time interval between each tick of the state machine clock (in minutes)
        :param accelerated: Don't wait for the time interval
        """
        self.__start_state_name = start_state_name
        self.__end_state_name = end_state_name
        self.__interval = interval
        self.__accelerated = accelerated
        self.__ticks = 0    # Track state machine ticks or state changes.
        self.__states = {}  # Contains the states to be run.
        self.__counts = {}  # Counts of how many times each state is reached.

    def add_state(self, new_state: State) -> None:
        """
        Add a new state to this machine instance.
        :param new_state: State to add
        :return: No meaningful return
        """
        self.__states[new_state.get_name()] = new_state
        self.__counts[new_state.get_name()] = 0

    def run(self, data: Generic[T]) -> None:
        """
        Run the state machine.
        :param data: Object which informs the state transition on the next state.
        :return: No meaningful return
        """
        new_state_name = self.__start_state_name
        while new_state_name != self.__end_state_name:
            age_logger.debug("{0}".format(str(data)))
            state = self.__states[new_state_name]
            self.__counts[new_state_name] += 1
            new_state_name = state.transition(self.__interval, data)
            self.__ticks += 1
            if not self.__accelerated:
                sleep(self.__interval * 60)

    @staticmethod
    def __format_age_time(minutes: int) -> str:
        """
        Format minutes of age time.
        :param minutes: to format
        :return: String of minutes in HH:MM format
        """
        hours = minutes // 60
        minutes -= hours * 60
        return "{0:02d}:{1:02d}".format(hours, minutes)

    def __calc_stats(self, duration: int) -> [float, str]:
        """
        Calculate percentage and the rough daily equivalent of time spent for given duration.
        :param duration: to calculate stats for
        :return: Percentage and average time
        """
        percentage = duration / self.__ticks * 100
        time = self.__format_age_time(round(percentage * 24 * 60) // 100)
        return percentage, time

    def stats(self) -> None:
        """
        Log stats on time spent in each state.
        :return: No meaningful return
        """
        age_logger.set_complete()
        age_logger.info("Dumping states for state machine instance...\n{:>107}"
                        .format("State     : Time spent in state (% and rough daily equivalent)"))
        for state in self.__counts:
            percentage, time = self.__calc_stats(self.__counts[state])
            age_logger.info("{0:9} : {1:04.2f}% - {2}".format(state, percentage, time))
