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
    process = Popen(f"smartctl -i {usb_id}", stdout=PIPE)
    info, _ = process.communicate()
    return info
