import json
from subprocess import Popen, PIPE
from pbs2usb._utils.helpers import smart_log


class PBSCommands:
    def __init__(self, proc_hash, datastore, namespace, log, trustless, test) -> None:
        self.proc_hash = proc_hash
        self.datastore = datastore
        self.namespace = namespace
        self.log = log
        self.trustless = trustless
        self.test = test

    @smart_log
    def create_usb_datastore(self):
        """Create a temporary datastore for PBS to use the USB drive"""
        cmd = [
            "proxmox-backup-manager",
            "datastore",
            "create",
            self.proc_hash,
            f"/media/{self.proc_hash}",
            "--comment",
            '"This is a temporary Datastore and should be automatically deleted after the backup"',  # noqa: E501
            "--verify-new",
            "true",
        ]
        process = Popen(cmd)
        process.wait()

    @smart_log
    def remove_usb_datastore(self):
        """Remove the previously created USB datastore to free the mounpoint"""
        cmd = ["proxmox-backup-manager", "datastore", "remove", self.proc_hash]
        process = Popen(cmd)
        process.wait()

    @smart_log
    def pull_datastore_to_usb(self):
        if self.test:
            return
        cmd = [
            "proxmox-backup-manager",
            "pull",
            "for_auto_usb_backup",
            self.datastore,
            self.proc_hash,
        ]
        if self.namespace:
            cmd += ["--remote-ns", self.namespace]
        process = Popen(cmd)
        process.wait()

    @smart_log
    def verify_usb_datastore(self):
        if self.test:
            return
        cmd = ["proxmox-backup-manager", "verify", self.proc_hash]
        process = Popen(cmd)
        process.wait()

    def confirm_datastore_exist(self):
        process = Popen(
            [
                "proxmox-backup-manager",
                "datastore",
                "list",
                "--output-format",
                "json",
            ],
            stdout=PIPE,
        )
        datastores, _ = process.communicate()
        datastores_list = json.loads(datastores)
        return (
            len(
                [
                    x
                    for x in datastores_list
                    if x["name"] == self.datastore
                ]
            )
            == 1
        )


    @staticmethod
    def confirm_remote_exist():
        process = Popen(
            [
                "proxmox-backup-manager",
                "remote",
                "list",
                "--output-format",
                "json",
            ],
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
