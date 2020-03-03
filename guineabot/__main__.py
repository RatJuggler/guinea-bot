import click
import os.path

from click import Context, Option

from .smt_logging import configure_logging, smt_logger
from .guineapig import GuineaPig, SLEEPING, add_guinea_pig_states
from .statemachine import StateMachine
from .twitter_api import get_twitter_service


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


def build_guinea_pig_machine(duration: int, interval: int, accelerated: bool) -> StateMachine:
    """
    Initialise the state machine.
    :param duration: The number of days the bot should run for
    :param interval: The time between changes in state, in minutes
    :param accelerated: Don't run in real-time
    :return: StateMachine instance with states configured
    """
    sm = StateMachine(duration, interval, accelerated)
    add_guinea_pig_states(sm)
    return sm


@click.command(help="""
    Guinea Pig Twitter bot.
                    """)
@click.version_option()
@click.option('-a', '--accelerated', 'accelerated', default=False, is_flag=True,
              help="Don't run in pseudo real-time, forces quiet mode to prevent Twitter API rate limit triggering.",
              show_default=True)
@click.option('-d', '--duration', 'duration', type=click.IntRange(1, 2920),
              help="How many guinea pig days the bot should run for.", default=2000, show_default=True)
@click.option('-i', '--interval', 'interval', type=click.IntRange(1, 1440),
              help="The interval between changes in guinea pig activity (state), in minutes.", default=15, show_default=True)
@click.option('-l', '--log-level', 'level', type=click.Choice(["DEBUG", "INFO", "WARNING"]),
              help="Show additional logging information.", default="INFO", show_default=True)
@click.option('-p', '--photos-folder', 'photos', type=click.STRING, callback=validate_photos_folder,
              help="Folder containing photos to Tweet.", show_default=True)
@click.option('-q', '--quiet', 'quiet', default=False, is_flag=True,
              help="Run without invoking the Twitter API.", show_default=True)
def simulate_guinea_pig(accelerated: bool, duration: int, interval: int, photos: str, level: str, quiet: bool) -> None:
    """
    Guinea Pig Twitter bot.
    :param accelerated: Don't run in pseudo real-time
    :param duration: The number of days the bot should run for
    :param interval: The time between changes in state, in minutes
    :param photos: Optional path to folder containing photos to use in some Tweets
    :param level: Set a logging level; DEBUG, INFO or WARNING
    :param quiet: Run without invoking the Twitter API
    :return: No meaningful return.
    """
    configure_logging(level)
    smt_logger.info("Booting guinea pig...")
    if accelerated:
        smt_logger.info("Accelerated running, quiet mode enforced.")
        quiet = True
    gp_machine = build_guinea_pig_machine(duration, interval, accelerated)
    a_guinea_pig = GuineaPig(SLEEPING, 20, 10, 10, photos, get_twitter_service(quiet))
    smt_logger.info("It's alive!")
    gp_machine.run(SLEEPING, a_guinea_pig)
    gp_machine.stats()


if __name__ == "__main__":
    simulate_guinea_pig()
