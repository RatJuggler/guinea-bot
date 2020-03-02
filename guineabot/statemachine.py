import logging

from time import sleep
from typing import Callable, List, Generic, TypeVar

T = TypeVar('T')


class State:

    def transition(self, data: Generic[T]) -> str:
        pass


class StateMachine:

    def __init__(self, interval: int, days: int, accelerated: bool) -> None:
        self.__interval = interval
        self.__days = days
        self.__accelerated = accelerated
        self.__run_time = (self.__days * 24 * 60) // self.__interval
        self.__states = {}
        self.__counts = {}

    def add_state(self, name: str, handler: Callable, changes: List[int]) -> None:
        name = name.upper()
        self.__states[name] = handler(name, changes)
        self.__counts[name] = 0

    @staticmethod
    def __format_time(total_minutes: int) -> str:
        hours = total_minutes // 60
        minutes = total_minutes - (hours * 60)
        return "{0:02d}:{1:02d}".format(hours, minutes)

    def __format_days_time(self, ticks: int) -> str:
        total_minutes = ticks * self.__interval
        days = total_minutes // (24 * 60)
        total_minutes -= days * 24 * 60
        return "Day: {0:4,d} - {1}".format(days, self.__format_time(total_minutes))

    def run(self, start_state: str, data: Generic[T]) -> None:
        new_state = start_state
        for i in range(self.__run_time):
            logging.debug("{0} >> {1}".format(self.__format_days_time(i), str(data)))
            state = self.__states[new_state]
            self.__counts[new_state] += 1
            new_state = state.transition(data)
            if not self.__accelerated:
                sleep(self.__interval * 60)

    def stats(self) -> None:
        logging.info("Dumping stats...\n                                 State     : Time spent in state (% and daily avg.)")
        for state in self.__counts:
            percentage = self.__counts[state] / self.__run_time * 100
            average = self.__format_time(self.__counts[state] * self.__interval // self.__days)
            logging.info("{0:9} : {1:04.2f}% - {2}".format(state, percentage, average))
