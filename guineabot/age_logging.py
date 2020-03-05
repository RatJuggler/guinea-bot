import logging
from typing import Dict, TypeVar

T = TypeVar('T')

AGE = 'age'


class AgeLoggerAdapter(logging.LoggerAdapter):
    """
    Age logging adapter.
    Allows log messages to include the age.
    """

    def set_age(self, age: str) -> None:
        """
        Set string to represent the age.
        :param age: String to show for age
        :return: No meaningful return
        """
        self.extra = {AGE: age}

    def process(self, msg: str, kwargs: Dict[str, T]) -> [str, Dict[str, T]]:
        """
        Overrides LoggerAdapter method.
        :param msg: Log message
        :param kwargs: Arguments
        :return: Updated log message and arguments
        """
        return '{0} >> {1}'.format(self.extra[AGE], msg), kwargs


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
age_logger = AgeLoggerAdapter(logging.getLogger(), {AGE: 'INITIALISE'})


def configure_logging(loglevel: str) -> None:
    """
    Configure basic logging to the console.
    :param loglevel: level name from the command line or default
    :return: No meaningful return
    """
    if logging.getLevelName(loglevel) == "Level {0}".format(loglevel):
        raise ValueError('Invalid log level: %s' % loglevel)
    age_logger.setLevel(loglevel)
