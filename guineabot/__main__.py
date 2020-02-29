import click
import logging

from .statemachine import StateMachine
from .guineapig import GuineaPig, GuineaPigState


def configure_logging(loglevel: str) -> None:
    """
    Configure basic logging to the console.
    :param loglevel: level name from the command line or default
    :return: No meaningful return
    """
    if logging.getLevelName(loglevel) == "Level {0}".format(loglevel):
        raise ValueError('Invalid log level: %s' % loglevel)
    logging.basicConfig(level=loglevel, format='%(asctime)s - %(levelname)s - %(message)s')


def build_guinea_pig_machine() -> StateMachine:
    """
    Initialise the state machine.
    :return: StateMachine instance with states configured.
    """
    sm = StateMachine(15, 2000)
    sm.add_state("SLEEPING", GuineaPigState, [-20, 3, 1])
    sm.add_state("AWAKE", GuineaPigState, [5, 5, 2])
    sm.add_state("THINKING", GuineaPigState, [1, 3, 1])
    sm.add_state("EATING", GuineaPigState, [5, -10, 4])
    sm.add_state("DRINKING", GuineaPigState, [5, 5, -80])
    sm.add_state("WANDERING", GuineaPigState, [10, 10, 5])
    return sm


@click.command(help="""
    Guinea Pig Twitter bot.
                    """)
@click.version_option()
@click.option('-p', '--photos-folder', 'photos', type=click.STRING,
              help="The folder containing photos to Tweet.", default="~/Pictures", show_default=True)
@click.option('-l', '--log-level', 'level', type=click.Choice(["DEBUG", "INFO", "WARNING"]),
              help="Show additional logging information.", default="INFO", show_default=True)
def simulate_guinea_pig(photos: str, level: str) -> None:
    """
    Guinea Pig Twitter bot.
    :param photos: Folder containing photos to use in some Tweets.
    :param level: Set a logging level; DEBUG, INFO or WARNING
    :return: No meaningful return.
    """
    configure_logging(level)
    logging.info("Booting guinea pig...")
    gp_machine = build_guinea_pig_machine()
    a_guinea_pig = GuineaPig("SLEEPING", 20, 10, 10)
    logging.info("It's alive!")
    gp_machine.run(a_guinea_pig)
    gp_machine.stats()


if __name__ == "__main__":
    simulate_guinea_pig()
