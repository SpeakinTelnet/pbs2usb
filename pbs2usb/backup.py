from pbs2usb._utils.pbs_commands import PBSCommands
from pbs2usb._utils.system_commands import SystemCommands


def backup(
    syscmd: SystemCommands,
    pbscmd: PBSCommands,
):

    syscmd.create_usb_folder()

    syscmd.mount_usb()

    if syscmd.check_existing_chunk_in_usb():
        syscmd.append_datastore_config()
    else:
        pbscmd.create_usb_datastore()

    pbscmd.pull_datastore_to_usb()

    pbscmd.verify_usb_datastore()

    pbscmd.remove_usb_datastore()

    syscmd.umount_usb()

    syscmd.remove_usb_folder()
