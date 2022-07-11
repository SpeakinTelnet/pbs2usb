import logging
import re


def make_logger(logger_level: str):
    logging.basicConfig(
        level=getattr(logging, logger_level, None),
        format="%(asctime)s - %(name)s - %(levelname)s %(message)s",
    )
    return logging.getLogger("pbs2usb")


def verify_usb_format(usb_id):
    try:
        assert re.match("\/dev\/sd[a-z]", usb_id)  # noqa: W605
        return True
    except AssertionError:
        return False
