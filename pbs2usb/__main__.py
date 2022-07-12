"""Main module."""

import json
import random
from pbs2usb._utils.pbs_commands import PBSCommands
from pbs2usb.backup import backup
from pbs2usb._utils.parser import parser

from pbs2usb._utils.helpers import (
    make_logger,
    verify_usb_format,
)

from pbs2usb._utils.system_commands import SystemCommands

if __name__ == "__main__":

    args = parser.parse_args()

    usb_id = args.usb_id
    datastore = args.datastore
    namespace = args.namespace
    unattended = args.unattended
    trustless = args.trustless
    logger_level = args.logger.upper()

    if trustless:
        PBSCommands.trustless = True
        SystemCommands.trustless = True
        unattended = False
        logger_level = "DEBUG"

    log = make_logger(logger_level)

    PBSCommands.log = log
    SystemCommands.log = log

    process_hash = random.randbytes(8).hex()

    syscmd = SystemCommands(usb_id, process_hash)

    pbscmd = PBSCommands(process_hash, datastore, namespace)

    if not verify_usb_format(usb_id):
        log.critical(f"{usb_id} does not match the /dev/sdX pattern")
        exit(1)

    diskinfo = syscmd.get_disk_info()

    if not diskinfo:
        log.critical(f"{usb_id} not found. Please verify the /dev/sdX id")
        exit(1)

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
    In folder /media/{process_hash}
    And pull the data from {datastore}
    """
    if args.namespace:
        msg += f"\nUsing the following namespace: {', '.join(args.namespace)}"

    log.info(msg)

    if trustless:
        input("Continue? \nHit return to continue or CTRL+C to cancel")

    backup(syscmd, pbscmd)
