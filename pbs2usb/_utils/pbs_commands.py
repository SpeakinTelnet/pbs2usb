import json
from subprocess import Popen, PIPE
from typing import Optional


def create_usb_datastore(hash: str):
    """Create a temporary datastore for PBS to use the USB drive"""
    cmd = [
        "sudo",
        "proxmox-backup-manager",
        "datastore",
        "create",
        hash,
        f"/media/{hash}",
        "--comment",
        '"This is a temporary Datastore and should be automatically deleted after the backup"',  # noqa: E501
        "--verify-new",
        "true",
    ]
    process = Popen(cmd)
    process.wait()


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
        )
        == 1
    )


def remove_usb_datastore(hash: str):
    """Remove the previously created USB datastore to free the mounpoint"""
    cmd = ["sudo", "proxmox-backup-manager", "datastore", "remove", hash]
    process = Popen(cmd)
    process.wait()


def pull_datastore(hash: str, datastore: str, namespace: Optional[list] = None):
    cmd = [
        "sudo",
        "proxmox-backup-manager",
        "pull",
        "for_auto_usb_backup",
        datastore,
        hash,
    ]
    if namespace:
        cmd += ["--remote-ns", namespace]
    process = Popen(cmd)
    process.wait()


def verify_usb(datastore: str):
    cmd = ["proxmox-backup-manager", "verify", datastore]
    process = Popen(cmd)
    process.wait()
