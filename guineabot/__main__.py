import os
from random import randint

import click

from prometheus_client import start_http_server

from .age_logging import configure_logging, age_logger
from .guineapig import create_guinea_pig
from .guineapig_states import build_guinea_pig_machine, GUINEAPIG_STATES
from .metrics import Metrics
from .tweeter import create_tweeter
from .twitter_api import TwitterServiceLive


# noinspection PyUnusedLocal
def validate_name(ctx: click.Context, param: click.Option, value: str) -> str:
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
def test_twitter_tokens(ctx: click.Context, param: click.Option, value: bool):
    if not value or ctx.resilient_parsing:
        return
    try:
        TwitterServiceLive()
    except Exception:
        click.echo('Unable to verify Twitter credentials!')
        ctx.exit(1)
    click.echo('Twitter credentials verified.')
    ctx.exit()


@click.command(help="""
    Guinea Pig Twitter bot.
                    """)
@click.version_option()
@click.option('-n', '--name', 'name', type=click.STRING, callback=validate_name,
              help="The name of the guinea pig.", default="Holly", show_default=True)
@click.option('-h', '--house', 'house', type=click.Path(exists=True, file_okay=False, writable=True, resolve_path=True),
              help="Piggy house where the guinea pig is kept.", default=lambda: os.environ.get('HOME', ''),
              show_default="user home directory")
@click.option('-p', '--photos', 'photos', type=click.Path(exists=True, file_okay=False),
              help="Optional path to photos which can be Tweeted.")
@click.option('-d', '--duration', 'duration', type=click.IntRange(1, 2920),
              help="How many days the bot should run for (guinea pig lifespan), random if not set.", show_default=False)
@click.option('-i', '--interval', 'interval', type=click.IntRange(1, 1440),
              help="The interval between changes in state (guinea pig activity), in minutes.", default=15, show_default=True)
@click.option('-a', '--accelerated', 'accelerated', default=False, is_flag=True,
              help="Ignore the pauses between state changes, forces quiet mode to prevent Twitter API rate limit triggering.",
              show_default=True)
@click.option('-l', '--log-level', 'level', type=click.Choice(["DEBUG", "INFO", "WARNING"]),
              help="Show additional logging information.", default="INFO", show_default=True)
@click.option('-m', '--metrics', 'metrics', default=False, is_flag=True,
              help="Publish metrics on the internal state of the bot.", show_default=True)
@click.option('-o', '--port', 'port', type=click.IntRange(1, 65536), default=8000,
              help="Port that any published metrics will be available on.", show_default=True)
@click.option('-q', '--quiet', 'quiet', default=False, is_flag=True,
              help="Run without invoking the Twitter API.", show_default=True)
@click.option('-t', '--test', 'test', default=False, is_flag=True, is_eager=True, callback=test_twitter_tokens, expose_value=False,
              help="Test the Twitter access tokens and exit.", show_default=True)
def simulate_guinea_pig(name: str, house: str, photos: str, duration: int, interval: int, accelerated: bool, level: str,
                        metrics: bool, port: int, quiet: bool) -> None:
    """
    Guinea Pig Twitter bot.
    :param name: Name of the bot
    :param house: Where the guinea pig state file is kept
    :param photos: Optional path to photos to use in some Tweets
    :param duration: The number of days the bot should run for
    :param interval: The time between changes in state, in minutes
    :param accelerated: Don't run in pseudo real-time
    :param level: Set a logging level; DEBUG, INFO or WARNING
    :param metrics: Publish metrics on the internal state
    :param port: Port that any published metrics will be available on
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
    publisher = Metrics(GUINEAPIG_STATES) if metrics else None
    guinea_pig = create_guinea_pig(name, house, duration, tweeter, publisher)
    gp_machine = build_guinea_pig_machine(interval, accelerated)
    if metrics:
        age_logger.info("Starting metrics publisher on port {0}.".format(port))
        start_http_server(port)
    age_logger.info("It's alive!")
    gp_machine.run(guinea_pig)
    final_stats = gp_machine.stats()
    age_logger.set_complete()
    age_logger.info("Dumping stats for state machine instance..." + final_stats)
    tweeter.tweet(final_stats)


if __name__ == "__main__":
    simulate_guinea_pig()   # pragma: no cover
