import click
import logging
import os.path

from click import Context, Option

from twitter_api import TwitterService
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


# noinspection PyUnusedLocal
def validate_photos_folder(ctx: Context, param: Option, value: str) -> str:
    """
    Validate that the photos folder supplied exists, empty string is valid if no value supplied.
    :param ctx: see callbacks for click options
    :param param: see callbacks for click options
    :param value: see callbacks for click options
    :return: Validated photos folder otherwise a click.BadParameter exception is raised
    """
    if value is None:
        return ""
    if not os.path.isdir(value):
        raise click.BadParameter(value)
    return value


def build_guinea_pig_machine() -> StateMachine:
    """
    Initialise the state machine.
    :return: StateMachine instance with states configured
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
@click.option('-p', '--photos-folder', 'photos', type=click.STRING, callback=validate_photos_folder,
              help="Folder containing photos to Tweet.", show_default=True)
@click.option('-l', '--log-level', 'level', type=click.Choice(["DEBUG", "INFO", "WARNING"]),
              help="Show additional logging information.", default="INFO", show_default=True)
@click.option('-q', '--quiet', default=False, is_flag=True,
              help="Run without invoking the Twitter API.", show_default=True)
def simulate_guinea_pig(photos: str, level: str, quiet: bool) -> None:
    """
    Guinea Pig Twitter bot.
    :param photos: Optional path to folder containing photos to use in some Tweets
    :param level: Set a logging level; DEBUG, INFO or WARNING
    :param quiet: Run without invoking the Twitter API
    :return: No meaningful return.
    """
    configure_logging(level)
    logging.info("Booting guinea pig...")
    gp_machine = build_guinea_pig_machine()
    a_guinea_pig = GuineaPig("SLEEPING", 20, 10, 10, photos, TwitterService(quiet))
    logging.info("It's alive!")
    gp_machine.run("SLEEPING", a_guinea_pig)
    gp_machine.stats()


if __name__ == "__main__":
    simulate_guinea_pig()
