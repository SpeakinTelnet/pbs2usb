"""Main module."""

import json
import random
from pbs2usb._utils.pbs_commands import PBSCommands
from pbs2usb.backup import backup
from pbs2usb._utils.parser import parser

from pbs2usb._utils.helpers import make_logger, verify_prerequisite

from pbs2usb._utils.system_commands import SystemCommands

if __name__ == "__main__":

    # Populate the vars
    args = parser.parse_args()

    usb_id = args.usb_id
    datastore = args.datastore
    namespace = args.namespace
    unattended = args.unattended
    trustless = args.trustless
    test = args.test
    logger_level = args.logger.upper()

    if trustless:
        unattended = False
        logger_level = "DEBUG"

    log = make_logger(logger_level)

    # Create an "hash" to use as folder and datastore
    proc_hash = random.randbytes(8).hex()

    syscmd = SystemCommands(usb_id, proc_hash, log, trustless)

    pbscmd = PBSCommands(proc_hash, datastore, namespace, log, trustless, test)

    diskinfo = verify_prerequisite(syscmd)

    if not unattended:
        # Get the usb info and confirmation before proceeding
        confirm = input(
            json.dumps(diskinfo, indent=4)
            + "\n\n"
            + "Please confirm that this is the usb disk. Are you sure? [y/n]: "
        )
        # Abort on anything other than 'y'
        if confirm.lower().strip() != "y":
            log.error("Cancelling the backup process")
            exit(1)

    msg = f"""
    Will mount usb {usb_id}
    In folder /media/{proc_hash}
    And pull the data from {datastore}
    """
    if args.namespace:
        msg += f"Using the following namespace: {namespace}"

    log.info(msg)

    if trustless:
        input("Continue? \nHit return to continue or CTRL+C to cancel")

    backup(syscmd, pbscmd)
