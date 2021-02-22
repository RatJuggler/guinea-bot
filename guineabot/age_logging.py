import logging
from typing import Dict, TypeVar

T = TypeVar('T')

AGE = 'age'


class AgeLoggerAdapter(logging.LoggerAdapter):
    """
    Age logging adapter.
    Allows log messages to include the age.
    """

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

    def set_age(self, age: int) -> None:
        """
        Set string to represent the age.
        :param age: String to show for age
        :return: No meaningful return
        """
        minutes = age
        days = minutes // (24 * 60)
        minutes -= days * 24 * 60
        self.extra = {AGE: "Age: {0:d} - {1}".format(days, self.__format_age_time(minutes))}

    def set_initialise(self) -> None:
        """
        Set string for initialisation logging.
        :return: No meaningful return
        """
        self.extra = {AGE: "INITIALISE"}

    def set_complete(self) -> None:
        """
        Set string for completion logging.
        :return: No meaningful return
        """
        self.extra = {AGE: "COMPLETE"}

    def process(self, msg: str, kwargs: Dict[str, T]) -> [str, Dict[str, T]]:
        """
        Overrides LoggerAdapter method.
        :param msg: Log message
        :param kwargs: Arguments
        :return: Updated log message and arguments
        """
        return '{0} >> {1}'.format(self.extra[AGE], msg), kwargs


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
age_logger = AgeLoggerAdapter(logging.getLogger(), {AGE: '<...>'})


def configure_logging(loglevel: str = "INFO") -> None:
    """
    Configure basic logging to the console.
    :param loglevel: level name from the command line or default
    :return: No meaningful return
    """
    if logging.getLevelName(loglevel) == "Level {0}".format(loglevel):
        raise ValueError('Invalid log level: %s' % loglevel)
    age_logger.setLevel(loglevel)
    age_logger.set_initialise()
