from random import randint

import click
import os.path

from click import Context, Option

from .age_logging import configure_logging, age_logger
from .guineapig import create_guinea_pig
from .guineapig_states import build_guinea_pig_machine
from .tweeter import create_tweeter


# noinspection PyUnusedLocal
def validate_name(ctx: Context, param: Option, value: str) -> str:
    """
    Validate that the name is a reasonable length.
    :param ctx: see callbacks for click options
    :param param: see callbacks for click options
    :param value: see callbacks for click options
    :return: Validated name otherwise a click.BadParameter exception is raised
    """
    if value is None or len(value) > 20:
        raise click.BadParameter(value)
    return value


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


@click.command(help="""
    Guinea Pig Twitter bot.
                    """)
@click.version_option()
@click.option('-a', '--accelerated', 'accelerated', default=False, is_flag=True,
              help="Ignore the pauses between state changes, forces quiet mode to prevent Twitter API rate limit triggering.",
              show_default=True)
@click.option('-d', '--duration', 'duration', type=click.IntRange(1, 2920),
              help="How many days the bot should run for (guinea pig lifespan), random if not set.", show_default=False)
@click.option('-i', '--interval', 'interval', type=click.IntRange(1, 1440),
              help="The interval between changes in state (guinea pig activity), in minutes.", default=15, show_default=True)
@click.option('-l', '--log-level', 'level', type=click.Choice(["DEBUG", "INFO", "WARNING"]),
              help="Show additional logging information.", default="INFO", show_default=True)
@click.option('-n', '--name', 'name', type=click.STRING, callback=validate_name,
              help="Give the bot a name.", default="Holly", show_default=True)
@click.option('-p', '--photos-folder', 'photos', type=click.STRING, callback=validate_photos_folder,
              help="Folder containing photos to Tweet.", show_default=True)
@click.option('-q', '--quiet', 'quiet', default=False, is_flag=True,
              help="Run without invoking the Twitter API.", show_default=True)
def simulate_guinea_pig(accelerated: bool, name: str, duration: int, interval: int, photos: str, level: str, quiet: bool) -> None:
    """
    Guinea Pig Twitter bot.
    :param accelerated: Don't run in pseudo real-time
    :param name: Name of the bot.
    :param duration: The number of days the bot should run for
    :param interval: The time between changes in state, in minutes
    :param photos: Optional path to folder containing photos to use in some Tweets\\
    :param level: Set a logging level; DEBUG, INFO or WARNING
    :param quiet: Run without invoking the Twitter API
    :return: No meaningful return.
    """
    configure_logging(level)
    age_logger.info("Booting guinea pig '{0}'...".format(name))
    if accelerated:
        age_logger.info("Accelerated running, quiet mode enforced.")
        quiet = True
    if duration is None:
        duration = randint(1460, 2920)  # 4-8 years.
    age_logger.info("Bot duration (guinea pig lifespan): {0} days".format(duration))
    age_logger.info("State interval (changes in guinea pig activity): {0} minutes".format(interval))
    tweeter = create_tweeter(photos, quiet)
    guinea_pig = create_guinea_pig(name, duration, tweeter)
    gp_machine = build_guinea_pig_machine(interval, accelerated)
    age_logger.info("It's alive!")
    gp_machine.run(guinea_pig)
    final_stats = gp_machine.stats()
    age_logger.set_complete()
    age_logger.info("Dumping stats for state machine instance..." + final_stats)
    tweeter.tweet(final_stats)


if __name__ == "__main__":
    simulate_guinea_pig()
