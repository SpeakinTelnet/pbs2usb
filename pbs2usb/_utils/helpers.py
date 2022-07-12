import logging
import re


def make_logger(logger_level: str):
    """Get a basic logger utility"""
    logging.basicConfig(
        level=getattr(logging, logger_level, None),
        format="%(asctime)s - %(name)s - %(levelname)s %(message)s",
    )
    return logging.getLogger("pbs2usb")


def verify_usb_format(usb_id):
    """Verify that the usb follow the /dev/sdX format"""
    try:
        assert re.match("\/dev\/sd[a-z]", usb_id)  # noqa: W605
        return True
    except AssertionError:
        return False


def verify_prerequisite(syscmd):
    """Verify that everything is included before the backup"""

    # Confirm lshw is installed
    if not syscmd.check_if_lshw_is_included():
        syscmd.log.critical("lshw is not accessible, please confirm it is installed")
        exit(1)

    # confirm proxmox backup manager is accessible
    if not syscmd.check_if_pbs_is_included():
        msg = """
Can't access Proxmox-backup-manager, please confirm that:

1- You have sudo privilege
2- /usr/sbin is in $PATH (might not be required with "sudo")
        """
        syscmd.log.critical(msg)
        exit(1)

    # Check usb format is valid
    if not verify_usb_format(syscmd.usb_id):
        syscmd.log.critical(f"{syscmd.usb_id} does not match the /dev/sdX pattern")
        exit(1)

    # check drive exists
    diskinfo = syscmd.get_disk_info()
    if not diskinfo:
        syscmd.log.critical(f"{syscmd.usb_id} not found. Please verify the /dev/sdX id")
        exit(1)

    return diskinfo


def smart_log(func):
    """A wrapper to log and input on command"""
    funcname = func.__name__.replace("_", " ")

    def wrapper(self, *args, **kwargs):
        self.log.debug(f"Starting action: {funcname}")
        future = func(self, *args, **kwargs)
        if self.trustless:
            input(
                f"""Action {funcname} is done! Continue?
                Hit return to continue or CTRL+C to cancel"""
            )
        return future

    return wrapper
