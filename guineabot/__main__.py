import click
import logging
import os.path

from click import Context, Option

from .guineapig import GuineaPig
from .guineapig_state import GuineaPigState, SLEEPING, AWAKE, THINKING, EATING, DRINKING, WANDERING
from .statemachine import StateMachine
from .twitter_api import TwitterServiceQuiet, TwitterServiceLive


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


def build_guinea_pig_machine(duration: int, accelerated: bool) -> StateMachine:
    """
    Initialise the state machine.
    :param duration: The number of days the bot should run for
    :param accelerated: Don't run in real-time
    :return: StateMachine instance with states configured
    """
    sm = StateMachine(duration, 15, accelerated)
    sm.add_state(GuineaPigState(SLEEPING, [-20, 3, 1]))
    sm.add_state(GuineaPigState(AWAKE, [5, 5, 2]))
    sm.add_state(GuineaPigState(THINKING, [1, 3, 1]))
    sm.add_state(GuineaPigState(EATING, [5, -10, 4]))
    sm.add_state(GuineaPigState(DRINKING, [5, 5, -80]))
    sm.add_state(GuineaPigState(WANDERING, [10, 10, 5]))
    return sm


@click.command(help="""
    Guinea Pig Twitter bot.
                    """)
@click.version_option()
@click.option('-a', '--accelerated', 'accelerated', default=False, is_flag=True,
              help="Don't run in pseudo real-time, forces quiet mode to prevent Twitter API rate limit triggering.",
              show_default=True)
@click.option('-d', '--duration', type=click.IntRange(1, 2920),
              help="How many guinea pig days the bot should run for.", default=2000, show_default=True)
@click.option('-l', '--log-level', 'level', type=click.Choice(["DEBUG", "INFO", "WARNING"]),
              help="Show additional logging information.", default="INFO", show_default=True)
@click.option('-p', '--photos-folder', 'photos', type=click.STRING, callback=validate_photos_folder,
              help="Folder containing photos to Tweet.", show_default=True)
@click.option('-q', '--quiet', 'quiet', default=False, is_flag=True,
              help="Run without invoking the Twitter API.", show_default=True)
def simulate_guinea_pig(accelerated: bool, duration: int, photos: str, level: str, quiet: bool) -> None:
    """
    Guinea Pig Twitter bot.
    :param accelerated: Don't run in pseudo real-time
    :param duration: The number of days the bot should run for
    :param photos: Optional path to folder containing photos to use in some Tweets
    :param level: Set a logging level; DEBUG, INFO or WARNING
    :param quiet: Run without invoking the Twitter API
    :return: No meaningful return.
    """
    configure_logging(level)
    logging.info("Booting guinea pig...")
    if accelerated:
        logging.info("Accelerated running, quiet mode enforced.")
        quiet = True
    gp_machine = build_guinea_pig_machine(duration, accelerated)
    if quiet:
        service = TwitterServiceQuiet()
    else:
        service = TwitterServiceLive()
    a_guinea_pig = GuineaPig(SLEEPING, 20, 10, 10, photos, service)
    logging.info("It's alive!")
    gp_machine.run(SLEEPING, a_guinea_pig)
    gp_machine.stats()


if __name__ == "__main__":
    simulate_guinea_pig()
