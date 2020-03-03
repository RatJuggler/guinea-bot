import logging
from typing import Dict, TypeVar

T = TypeVar('T')

SMT = 'smt'


class SMTAdapter(logging.LoggerAdapter):
    """
    State Machine TIme logging adapter.
    Allows log messages to include an element driven by the number of ticks of the state machine.
    """

    def set_smt(self, smt: str) -> None:
        """
        Set string to represent the state machine time.
        :param smt: String to show for state machine time.
        :return: No meaningful return
        """
        self.extra = {SMT: smt}

    def process(self, msg: str, kwargs: Dict[str, T]) -> [str, Dict[str, T]]:
        """
        Overrides LoggerAdapter method.
        :param msg: Log message
        :param kwargs: Arguments
        :return: Updated log message and arguments
        """
        return '{0} >> {1}'.format(self.extra[SMT], msg), kwargs


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
smt_logger = SMTAdapter(logging.getLogger(), {SMT: 'INITIALISE'})


def configure_logging(loglevel: str) -> None:
    """
    Configure basic logging to the console.
    :param loglevel: level name from the command line or default
    :return: No meaningful return
    """
    if logging.getLevelName(loglevel) == "Level {0}".format(loglevel):
        raise ValueError('Invalid log level: %s' % loglevel)
    smt_logger.setLevel(loglevel)
