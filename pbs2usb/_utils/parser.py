import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "usb_id",
    metavar="USB /dev/sdX",
    nargs="?",
    help="ID of the USB drive to backup to as /dev/sdX",
)

parser.add_argument("datastore", nargs="?", help="Datastore to pull the backup from")

parser.add_argument(
    "--namespace", dest="namespace", nargs="?", help="Specify a namespace to backup"
)

parser.add_argument(
    "--unattended",
    dest="unattended",
    action="store_true",
    help="""Remove the USB drive confirmation""",
)

parser.add_argument(
    "--trustless",
    dest="trustless",
    action="store_true",
    help="""Will required confirmation at each step,
                            Overwrite --unattended""",
)

parser.add_argument(
    "--logger",
    dest="logger",
    nargs="?",
    default="INFO",
    choices=("CRITICAL", "FATAL", "ERROR", "WARNING", "WARN", "INFO", "DEBUG"),
    help="Logging level desired",
)
