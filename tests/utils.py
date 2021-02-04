from testfixtures import LogCapture

import guineabot.age_logging as al


def log_check(log_out: LogCapture, *expects: str) -> None:
    root = "root"
    log_level = al.logging.getLevelName(al.logging.INFO)
    for expected in expects:
        log_out.check_present((root, log_level, expected))
