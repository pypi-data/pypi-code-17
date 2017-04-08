#!/usr/bin/env python

# Automatically make Constantine posters in term time.
# Helper script useful for cron jobs.

import os
import datetime
import subprocess
import sys

from Constantine import utils

MAIN_TIMEOUT = 15

if (not 2 <= len(sys.argv) <= 5) or (sys.argv[1] in ['-h', '--help']):
    print("Usage: python auto_poster.py /path/to/output.pdf [options]")
    print("Helper script useful for cron jobs. Pass in the directory of Constantine's main.py for working directory purposes.")
    print("Options:")
    print("--date=YYYY-MM-DD : Provide a date as the second argument to fetch the calendar for the following week of that date (not for the week the date is in!) e.g. 2017-02-01 | Default: Today's date.")
    print("--text=/path/to/special/text.txt : Provide a custom path to the special text file to be included in the poster. | Default: special_text.txt under the script directory.")
    print("--config=/path/to/settings.json : The path to settings.json for configuring Constantine. | Default: the settings.json under the script directory, which may be strange if you installed Constantine with pip.")
    print("See Docs/settings-example.json for an example.")
    print()
    sys.exit(1)

constantine_directory = utils.get_project_full_path()
output_file = sys.argv[1]
set_date = datetime.datetime.today()
text_file_path = utils.get_project_full_path() + "/special_text.txt"
config_file_path = utils.get_project_full_path() + "/settings.json"
if len(sys.argv) > 2:
    for argv in sys.argv[2:]:

        # Date.
        if (not argv.startswith('--')) or argv.startswith('--date='):
            # Support old options format.
            if argv.startswith('--date='):
                set_date = argv[7:]
            else:
                set_date = argv

            if not utils.check_date_string(set_date):
                print("Error: the date you have set is invalid, it must be in YYYY-MM-DD form such as 2017-02-01.")
                sys.exit(1)
            else:
                set_date = datetime.datetime.strptime(set_date, "%Y-%m-%d")

        # Special text.
        if argv.startswith('--text='):
            text_file_path = argv[7:]
            if text_file_path.startswith('~'):
                text_file_path = os.path.expanduser('~') + '/' + text_file_path[1:]

        # Settings file.
        if argv.startswith('--config='):
            config_file_path = argv[9:]
            if config_file_path.startswith('~'):
                config_file_path = os.path.expanduser('~') + '/' + config_file_path[1:]

settings = utils.read_config(config_file_path)

next_monday = set_date + datetime.timedelta(days=(7 - set_date.weekday()))
term_start = datetime.datetime.strptime(utils.get_closest_date_time(next_monday, settings['term_start_dates']), "%Y-%m-%d")
date_param = datetime.datetime.strftime(set_date, "%Y-%m-%d")
week_number = int((next_monday - term_start).days / 7 + 1)

if (1 <= week_number <= 10):
    print("Running Constantine for Week " + str(week_number) + ".")
    p = subprocess.Popen(['python', 'main.py', output_file, "--date=" + date_param, "--text=" + text_file_path, "--config=" + config_file_path], stdout=subprocess.PIPE, cwd=constantine_directory)
    output = p.communicate(timeout=MAIN_TIMEOUT)
    print("Finished with code " + str(p.returncode))
    sys.exit(p.returncode) # Exit with the same code for monitoring purposes.
else:
    print("Not term time, not updating the PDF.")
    sys.exit(0)
