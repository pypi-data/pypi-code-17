import logging
import signal
import time
import sys
import yaml

from collector import Collector
from processor import Processor
from rules import parse_rules_from_file
from watcher import Watcher
from rundb.client import RunDbc


def parse_config(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)


def parse_args():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--rules', help='Path to rules file', required=True)
    parser.add_argument('--config', help='Path to rules file', required=True)
    parser.add_argument('--log', help='Path to log file')
    return parser.parse_args()


def main():
    args = parse_args()

    settings_file = args.config
    rules_file = args.rules

    settings = parse_config(settings_file)

    rules = parse_rules_from_file(rules_file)

    search = RunDbc(settings['runDB']['API_key'], settings['runDB']['host'])

    root = logging.getLogger()
    root.setLevel(logging.INFO)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)
    if args.log:
        file_log = logging.FileHandler(args.log)
        file_log.setLevel(logging.INFO)
        file_log.setFormatter(formatter)
        root.addHandler(file_log)

    col = Collector()

    watchers = []
    timeout = int(settings['watch']['timeout'])
    for d in settings['watch']['directories']:
        w = Watcher(d, timeout)
        col.attach(w)
        w.run()
        watchers.append(w)

    processor = Processor(search, rules, settings['hostname'])
    processor.attach_collector(col)

    def sighup_handler(_, __):
        log = logging.getLogger("SIGHUP")
        log.info("Received SIGHUP. Reloading {} and {}".format(rules_file, settings_file))
        try:
            processor.set_rules(parse_rules_from_file(rules_file))
        except Exception as e:
            log.error("Failed reloading rules due to: {}".format(e.message))

    signal.signal(signal.SIGHUP, sighup_handler)

    while True:
        time.sleep(1000)


if __name__ == '__main__':

    main()


