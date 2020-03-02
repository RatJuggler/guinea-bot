import logging

from time import sleep
from typing import Generic, TypeVar

T = TypeVar('T')


class State:
    """
    States are used to configure the StateMachine.
    """

    def get_name(self) -> str:
        """
        The states name.
        :return: State name
        """
        pass

    def transition(self, data: Generic[T]) -> str:
        """
        A transition to the next state.
        :param data: Object which informs the transition on the next state.
        :return: The next state (not necessarily different to the current state)
        """
        pass


class StateMachine:
    """
    A pseudo real-time state machine which runs for a fixed duration of days and transitions to the next state after each fixed
    interval of minutes.
    """

    def __init__(self, duration: int, interval: int, accelerated: bool) -> None:
        """
        Initialise a StateMachine instance.
        :param duration: How long the state machine will run for in days
        :param interval: The time interval between state transitions in minutes
        :param accelerated: Don't wait for the time interval
        """
        self.__duration = duration
        self.__interval = interval
        self.__accelerated = accelerated
        # Calculate the number of interval ticks over the duration.
        self.__ticks = (self.__duration * 24 * 60) // self.__interval
        self.__states = {}
        self.__counts = {}

    def add_state(self, new_state: State) -> None:
        """
        Add a new state to this machine instance.
        :param new_state: State to add
        :return: No meaningful return
        """
        name = new_state.get_name()
        self.__states[name] = new_state
        self.__counts[name] = 0

    @staticmethod
    def __format_time(total_minutes: int) -> str:
        """
        Format total minutes
        :param total_minutes: to format
        :return: String of total minutes in HH:MM format
        """
        hours = total_minutes // 60
        minutes = total_minutes - (hours * 60)
        return "{0:02d}:{1:02d}".format(hours, minutes)

    def __format_days_time(self, tick: int) -> str:
        """
        Format tick into days, hours and minutes
        :param tick: The tick of elapsed intervals
        :return: String of ticks in DD - HH:MM format
        """
        total_minutes = tick * self.__interval
        days = total_minutes // (24 * 60)
        total_minutes -= days * 24 * 60
        return "Day: {0:4,d} - {1}".format(days, self.__format_time(total_minutes))

    def run(self, start_state: str, data: Generic[T]) -> None:
        """
        Run the state machine.
        :param start_state: Initial state
        :param data: Object which informs the state transition on the next state.
        :return: No meaningful return
        """
        new_state = start_state
        for tick in range(self.__ticks):
            logging.debug("{0} >> {1}".format(self.__format_days_time(tick), str(data)))
            state = self.__states[new_state]
            self.__counts[new_state] += 1
            new_state = state.transition(data)
            if not self.__accelerated:
                sleep(self.__interval * 60)

    def stats(self) -> None:
        """
        Log stats on time spent in each state.
        :return: No meaningful return
        """
        logging.info("Dumping stats...\n                                 State     : Time spent in state (% and daily avg.)")
        for state in self.__counts:
            percentage = self.__counts[state] / self.__ticks * 100
            average = self.__format_time(self.__counts[state] * self.__interval // self.__duration)
            logging.info("{0:9} : {1:04.2f}% - {2}".format(state, percentage, average))
