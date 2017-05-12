import argparse
import logging

import logger
from monitor import Monitor


parser = argparse.ArgumentParser()
parser.add_argument("-c", "--compose-file", dest="path",
    default=".", help="Path to the docker-compose.yml")
parser.add_argument("-t", "--timeout", dest="timeout",
    default=10, help="Check&update timeout")
parser.add_argument("-o", "--options", dest="options",
    nargs='+', help="Options for project")
parser.add_argument("-l", "--log", dest="log",
    help="Redirect logging to file")
args = parser.parse_args()

if args.log is not None:
    log = logging.getLogger(__name__)
    log.addHandler(logger.FileHandler(args.log))
    log.setLevel(logging.DEBUG)
else:
    log = logging.getLogger(__name__)
    log.addHandler(logger.StreamHandler())
    log.setLevel(logging.DEBUG)


def main():
    try:
        if args.options is None:
            monitor = Monitor(args.path, dict(), args.log)
        else:
            monitor = Monitor(args.path,
                dict(zip(args.options[0::2], args.options[1::2])), args.log)
        log.info("Monitor created successfully")

        log.info("Starting of monitor...")
        monitor.run(int(args.timeout))

    except KeyboardInterrupt:
        print('\nThe process was interrupted by the user')
        raise SystemExit

if __name__ == "__main__":
    main()
