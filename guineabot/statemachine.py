import logging

from time import sleep
from typing import Callable, List


class State:

    def transition(self, data) -> str:
        pass


class StateMachine:

    def __init__(self, interval: int, days: int) -> None:
        self.interval = interval
        self.days = days
        self.run_time = (self.days * 24 * 60) // self.interval
        self.states = {}
        self.counts = {}

    def add_state(self, name: str, handler: Callable, changes: List[int]) -> None:
        name = name.upper()
        self.states[name] = handler(name, changes)
        self.counts[name] = 0

    @staticmethod
    def __format_time(total_minutes: int) -> str:
        hours = total_minutes // 60
        minutes = total_minutes - (hours * 60)
        return "{0:02d}:{1:02d}".format(hours, minutes)

    def __format_days_time(self, ticks: int) -> str:
        total_minutes = ticks * self.interval
        days = total_minutes // (24 * 60)
        total_minutes -= days * 24 * 60
        return "Day: {0:4,d} - {1}".format(days, self.__format_time(total_minutes))

    def run(self, start_state: str, data) -> None:
        new_state = start_state
        for i in range(self.run_time):
            logging.info("{0} >> {1}".format(self.__format_days_time(i), str(data)))
            state = self.states[new_state]
            self.counts[new_state] += 1
            new_state = state.transition(data)
            sleep(self.interval * 60)

    def stats(self) -> None:
        logging.info("\n\n\nState     : Time spent in state (% and daily avg.)")
        for state in self.counts:
            percentage = self.counts[state] / self.run_time * 100
            average = self.__format_time(self.counts[state] * self.interval // self.days)
            logging.info("{0:9} : {1:04.2f}% - {2}".format(state, percentage, average))
