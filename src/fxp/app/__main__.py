import os
import signal
import argparse

import time

ROOT_DIR = os.path.abspath(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                __file__
                )
            )
        )
    )
)
#print(ROOT_DIR)

def get_version():
    with open(os.path.join(ROOT_DIR, "VERSION")) as  version_file:
        return version_file.read().strip()

def create_parser():
    parser = argparse.ArgumentParser(
        prog="Forex parser",
        description="(c) 2021 TMS",
        add_help=False,
    )
    parser.add_argument(
        "-h",
        "--help",
        action="help",
        help="Print this message.",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        help="Current version.",
        version=get_version(),
    )
    parser.add_argument(
        "-d",
        "--deamon",
        action="store_true",
        required=False,
        help="Load the application as a deamon."
    )
    parser.add_argument(
        "-k",
        "--kill",
        action="store_true",
        help="Stop the application."
    )
    parser.add_argument(
        "-p",
        "--pid",
        dest="pid_file",
        help="Name of pid file.",
        default="/tmp/fxp.pid"
    )
    return parser

parser = create_parser()
args = parser.parse_args()
print(args)

WORK = True

def stop_handler(signum, frame):
    # print(signal.SIGTERM.value)
    # print(frame)
    # print(type(frame))
    global WORK
    WORK = False

def start():
    log = open(os.path.join(ROOT_DIR, ".log.log"), "a")
    while WORK:
        log.writelines(["I'm working.\n"])
        #print("I'm working.")
        time.sleep(2)
    else:
        log.write("Stop.\n")
        #print("Stop.")

def stop():
    if os.path.isfile(args.pid_file):
        with open(args.pid_file, "r") as pid_file:
            pid = int(pid_file.read().strip())
        os.kill(pid, signal.SIGTERM)
    else:
        print("Not found.")

if args.deamon and args.kill:
    raise RuntimeError("or deamon or kill.")

if args.deamon:
    if os.path.isfile(args.pid_file):
        print("Server is working.")
        exit(1)
    if not os.path.isdir(
        os.path.abspath(os.path.dirname(args.pid_file)),
    ):
        os.makedirs(
            os.path.abspath(os.path.dirname(args.pid_file)),
        )
    pid = os.fork()
    if not pid:
        with open(args.pid_file, "w") as pid_file:
            pid_file.write(str(os.getpid()))
        #print(dir(signal).SIGTERM.value)
        signal.signal(signal.SIGTERM, stop_handler)
        start()
    else:
        print(pid)
elif args.kill:
    stop()
    os.unlink(args.pid_file)
    exit(0)
else:
    try:
        start()
    except KeyboardInterrupt:
        WORK = False