"""Main module."""

import random
from pbs2usb.backup import backup
from pbs2usb._utils.parser import parser

from pbs2usb._utils.helpers import (
    make_logger,
    verify_usb_format,
)

from pbs2usb._utils.system_commands import get_disk_info

if __name__ == "__main__":

    args = parser.parse_args()

    usb_id = args.usb_id
    datastore = args.datastore
    namespace = args.namespace
    unattended = args.unattended
    trustless = args.trustless
    logger_level = args.logger.upper()

    if trustless:
        unattended = False
        logger_level = "DEBUG"

    log = make_logger(logger_level)

    if not verify_usb_format(usb_id):
        log.critical(f"{usb_id} does not match the /dev/sdX pattern")
        exit(1)

    diskinfo = get_disk_info(usb_id)

    if "failed: No such device" in diskinfo:
        log.critical(f"{usb_id} not found. Please verify the /dev/sdX id")
        exit(1)

    if not unattended:
        # Get the usb info and confirmation before proceeding
        confirm = input(
            diskinfo
            + "\n\n"
            + "Please confirm that this is the usb disk. Are you sure? [y/n]: "
        )
        # Abort on anything other than 'y'
        if confirm.lower().strip() != "y":
            log.error("Cancelling the backup process")
            exit(1)

    process_hash = random.randbytes(32).hex()

    msg = """
    Will mount usb {usb_id}
    In folder /media/{process_hash}
    And pull the data from {datastore}
    """
    if args.namespace:
        msg += f"\nUsing the following namespace: {', '.join(args.namespace)}"

    log.info(msg)

    if trustless:
        input("Continue? \nHit return to continue or CTRL+C to cancel")

    backup(log, process_hash, usb_id, datastore, trustless, namespace)
