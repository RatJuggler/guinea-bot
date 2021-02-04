from testfixtures import LogCapture

from guineabot.age_logging import logging


def log_check(log_out: LogCapture, *expects: str) -> None:
    root = "root"
    log_level = logging.getLevelName(logging.INFO)
    for expected in expects:
        log_out.check_present((root, log_level, expected))
