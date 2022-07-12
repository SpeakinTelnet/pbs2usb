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
    "--loglevel",
    dest="loglevel",
    nargs="?",
    default="INFO",
    choices=("CRITICAL", "FATAL", "ERROR", "WARNING", "WARN", "INFO", "DEBUG"),
    help="Logging level desired",
)

parser.add_argument(
    "--test",
    dest="test",
    action="store_true",
    help="""Will not run pull/verify on the datastore, use to test workflow""",
)