from logging import Logger
from typing import Optional

from pbs2usb._utils.pbs_commands import (
    create_usb_datastore,
    remove_usb_datastore,
    pull_datastore,
    verify_usb,
)
from pbs2usb._utils.system_commands import (
    mount_usb,
    umount_usb,
    create_folder,
    remove_folder,
)


def cleanup(usb_id: str, process_hash: str):
    remove_usb_datastore(process_hash)
    umount_usb(usb_id, process_hash)
    remove_folder(process_hash)


def confirmation(trustless):
    if trustless:
        input("Done! Continue? \nHit return to continue or CTRL+C to cancel")


def backup(
    log: Logger,
    process_hash: str,
    usb_id: str,
    datastore: str,
    trustless: bool,
    namespace: Optional[list] = None,
):

    log.debug("Creating USB folder")
    create_folder(process_hash)
    confirmation(trustless)

    log.debug("Creating USB datastore")
    create_usb_datastore(process_hash)
    confirmation(trustless)

    log.debug("Mounting USB")
    mount_usb(usb_id, process_hash)
    confirmation(trustless)

    log.debug("Pulling backup")
    pull_datastore(process_hash, datastore, namespace)
    confirmation(trustless)

    log.debug("Verifying the USB backup")
    verify_usb(datastore)
    confirmation(trustless)

    log.debug("Cleaning up!")
    cleanup(usb_id, process_hash)
