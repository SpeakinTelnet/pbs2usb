"""Main module."""

import random
from pbs2usb._utils.pbs_commands import PBSCommands
from pbs2usb.backup import backup
from pbs2usb._utils.parser import parser

from pbs2usb._utils.helpers import make_logger, verify_prerequisite

from pbs2usb._utils.system_commands import SystemCommands


def main():

    # Populate the vars
    args = parser.parse_args()

    usb_id = args.usb_id
    datastore = args.datastore
    namespace = args.namespace
    unattended = args.unattended
    trustless = args.trustless
    test = args.test
    logger_level = args.loglevel.upper()

    if trustless:
        unattended = False
        logger_level = "DEBUG"

    log = make_logger(logger_level)

    # Create an "hash" to use as folder and datastore
    hex_bytes = random.randbytes(8).hex()

    syscmd = SystemCommands(usb_id, hex_bytes, log, trustless)

    pbscmd = PBSCommands(hex_bytes, datastore, namespace, log, trustless, test)

    diskinfo = verify_prerequisite(syscmd)

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

    msg = f"""
    Will mount usb {usb_id}
    In folder /media/{hex_bytes}
    And pull the data from {datastore}
    """
    if args.namespace:
        msg += f"Using the following namespace: {namespace}"

    log.info(msg)

    if trustless:
        input("Continue? \nHit return to continue or CTRL+C to cancel")

    backup(syscmd, pbscmd)


if __name__ == "__main__":
    main()
