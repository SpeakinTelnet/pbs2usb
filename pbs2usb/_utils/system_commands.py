import json
import os
from subprocess import Popen, PIPE
from pbs2usb._utils.helpers import smart_log


class SystemCommands:


    def __init__(self, usb_id, hash, log, trustless) -> None:
        self.usb_id = usb_id
        self.hash = hash
        self.log = log
        self.trustless = trustless

    @smart_log
    def mount_usb(self):
        Popen(["sudo", "mount", self.usb_id, f"/media/{hash}"]).wait()

    @smart_log
    def umount_usb(self):
        Popen(["sudo", "umount", self.usb_id, f"/media/{self.hash}"]).wait()

    @smart_log
    def create_usb_folder(self):
        Popen(["mkdir", f"/media/{self.hash}"]).wait()

    @smart_log
    def remove_usb_folder(self):
        Popen(["rm", "-r", f"/media/{self.hash}"]).wait()

    @smart_log
    def append_datastore_config(self):
        datastore_add = f"""
        datastore: {self.hash}
            path /media/{self.hash}
        """
        with open("/etc/proxmox-backup/datastore.cfg", "a") as file:
            file.write(datastore_add)


    def check_existing_chunk_in_usb(self):
        path = f"/media/{self.hash}/.chunks"
        return os.path.exists(path)

    
    def get_disk_info(self):
        process = Popen(["lshw", "-c", "disk", "-json", "-quiet"], stdout=PIPE)
        json_disks, _ = process.communicate()
        disks = json.loads(json_disks)
        for disk in disks:
            if self.usb_id in disk["logicalname"]:
                return disk 
