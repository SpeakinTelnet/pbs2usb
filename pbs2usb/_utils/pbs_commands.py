import json
from subprocess import Popen, PIPE
from typing import Optional
from pbs2usb._utils.helpers import smart_log


class PBSCommands:

    log = None
    trustless = False
    
    def __init__(self, hash, datastore, namespace = None) -> None:
        self.hash = hash
        self.datastore = datastore
        self.namespace = namespace


    @smart_log(trustless, log)
    def create_usb_datastore(self):
        """Create a temporary datastore for PBS to use the USB drive"""
        cmd = [
            "sudo",
            "proxmox-backup-manager",
            "datastore",
            "create",
            self.hash,
            f"/media/{self.hash}",
            "--comment",
            '"This is a temporary Datastore and should be automatically deleted after the backup"',  # noqa: E501
            "--verify-new",
            "true",
        ]
        process = Popen(cmd)
        process.wait()


    @smart_log(trustless, log)
    def remove_usb_datastore(self):
        """Remove the previously created USB datastore to free the mounpoint"""
        cmd = ["sudo", "proxmox-backup-manager", "datastore", "remove", self.hash]
        process = Popen(cmd)
        process.wait()


    @smart_log(trustless, log)
    def pull_datastore_to_usb(self):
        cmd = [
            "sudo",
            "proxmox-backup-manager",
            "pull",
            "for_auto_usb_backup",
            self.datastore,
            self.hash,
        ]
        if self.namespace:
            cmd += ["--remote-ns", self.namespace]
        process = Popen(cmd)
        process.wait()


    @smart_log(trustless, log)
    def verify_usb_datastore(self):
        cmd = ["proxmox-backup-manager", "verify", self.datastore]
        process = Popen(cmd)
        process.wait()

    @staticmethod
    def confirm_remote_exist():
        process = Popen(
            ["sudo", "proxmox-backup-manager", "remote", "list", "--output-format", "json"],
            stdout=PIPE,
        )
        remotes, _ = process.communicate()
        remotes_list = json.loads(remotes)
        return (
            len(
                [
                    x
                    for x in remotes_list
                    if x["name"] == "for_auto_usb_backup" and x["host"] == "127.0.0.1"
                ]
            ) == 1
        )
