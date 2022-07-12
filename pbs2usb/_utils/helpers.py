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

def smart_log(trustless, log):
    def _smart_log(func):
        funcname = func.__name__.replace('_', ' ')
        def wrapper(*args, **kwargs):
            log.debug(f"Starting action: {funcname}")
            future = func(*args, **kwargs)
            if trustless:
                input(f"""Action {funcname} is done! Continue?
                    Hit return to continue or CTRL+C to cancel""")
            return future
        return wrapper
    return _smart_log
