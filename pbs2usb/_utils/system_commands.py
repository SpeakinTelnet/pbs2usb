import json
from subprocess import Popen, PIPE


def mount_usb(usb_id: str, hash: str):
    Popen(["sudo", "mount", usb_id, f"/media/{hash}"]).wait()


def umount_usb(usb_id: str, hash: str):
    Popen(["sudo", "umount", usb_id, f"/media/{hash}"]).wait()


def create_folder(hash: str):
    Popen(["mkdir", f"/media/{hash}"]).wait()


def remove_folder(hash: str):
    Popen(["rm", "-r", f"/media/{hash}"]).wait()


def get_disk_info(usb_id):
    process = Popen(["lshw", "-c", "disk", "-json", "-quiet"], stdout=PIPE)
    json_disks, _ = process.communicate()
    disks = json.loads(json_disks)
    for disk in disks:
        if usb_id in disk["logicalname"]:
            return disk 
