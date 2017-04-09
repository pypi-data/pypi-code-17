#!/usr/bin/env python
# Too little time, far from my proper Python.

import os
import sys
import subprocess
import time
import datetime

from Constantine import utils
import requests

def run(args):
    GOOGLE_CALENDAR_API = "https://www.googleapis.com/calendar/v3/calendars/"
    DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    XELATEX_TIMEOUT = 15

    if (not 2 <= len(sys.argv) <= 5) or (sys.argv[1] in ['-h', '--help']):
        print("Usage: python main.py /path/to/output.pdf [options]")
        print("Options:")
        print("--date=YYYY-MM-DD : Provide a date as the second argument to fetch the calendar for the following week of that date (not for the week the date is in!) e.g. 2017-02-01 | Default: Today's date.")
        print("--text=/path/to/special/text.txt : Provide a custom path to the special text file to be included in the poster. | Default: special_text.txt under the script directory.")
        print("--config=/path/to/settings.json : The path to settings.json for configuring Constantine. | Default: the settings.json under the script directory, which may be strange if you installed Constantine with pip.")
        print("See Docs/settings-example.json for an example.")
        sys.exit(1)

    # Process date param.
    set_date = datetime.datetime.today()
    text_file_path = utils.get_project_full_path() + "/special_text.txt"
    config_file_path = None

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
                    config_file_path = os.path.expanduser('~') + '/' + text_file_path[1:]

    output_dir = sys.argv[1].rsplit('/', 1)[0]
    output_file = sys.argv[1]

    if '/' not in output_file: # Current directory.
        output_dir = './'
        output_file = './' + output_file

    if not os.path.isdir(output_dir):
        print("The directory " + output_dir + " does not exist, exiting.")
        sys.exit(1)

    print("Reading settings.json...")
    settings = utils.read_config(config_file_path)

    # Find out which week is the next week we are working on.
    next_monday = set_date + datetime.timedelta(days=(7 - set_date.weekday()))
    monday_after = next_monday + datetime.timedelta(days=7)
    start_date = next_monday.strftime("%Y-%m-%d") + "T00:00:00Z"
    end_date = monday_after.strftime("%Y-%m-%d") + "T00:00:00Z"
    term_start = datetime.datetime.strptime(utils.get_closest_date_time(next_monday, settings['term_start_dates']), "%Y-%m-%d")
    week_number = int((next_monday - term_start).days / 7 + 1)

    # Fetch data.
    request_url = GOOGLE_CALENDAR_API + settings['calendar_id'] + "/events"
    request_params = {'key': settings['google_api_key'], 'orderBy': 'startTime', 'singleEvents': 'true', 'timeMin': start_date, 'timeMax': end_date}
    print("Reading calendar events for week starting {}...".format(next_monday.strftime("%Y-%m-%d")))
    api_response = requests.get(request_url, params=request_params)
    if api_response.status_code != 200:
        print("Error fetching calendar data from Google, check your network connection and API key.\
            If you have a valid API key, it may be missing Google Calendar Access.")
        sys.exit(1)
    events = api_response.json()

    # Organise data.
    events_organised = {DAYS.index(i):[] for i in DAYS}
    for event in events['items']:

        if any([(i not in event) for i in ['start', 'summary', 'location']]):
            continue # Just in case a broken event returned in json.

        event_date = event['start']['dateTime']
        datetime_split = event_date.split('T')
        event_datetime = datetime.datetime.strptime(datetime_split[0], "%Y-%m-%d")
        event_start = datetime_split[1][:5]
        event_day = int((event_datetime - next_monday).days) + 1
        event_item = {}
        event_item['what'] = utils.tex_escape(event['summary'])
        event_item['when'] = utils.tex_escape(event_start)
        event_item['where'] = utils.tex_escape(event['location'])
        events_organised[event_day].append(event_item)

    # Read from and format the templates.
    print("Generating LaTeX file from template...")
    with open(utils.get_project_full_path() + "/latex_template.txt", 'r') as template_file:
        latex_template = template_file.read()

    try:
        with open(text_file_path, 'r') as special_file:
            special_text_lines = special_file.readlines()
    except FileNotFoundError:
        print("Error: special text file " + text_file_path + " cannot be found, the PDF cannot be generated. Exiting.")
        sys.exit(1)

    latex_formatting = utils.settings_to_formatting(settings)
    latex_formatting['week_number'] = str(week_number)
    event_content = ""
    for day, day_events in events_organised.items():

        if len(day_events) < 1:
            continue

        day_tex = "\\begin{minipage}{0.5\\textwidth}{\\fontsize{30}{40}\\selectfont %s}\\\\\\vspace{0.2cm}\\begin{addmargin}[1em]{0em}" % (DAYS[day])
        for day_event in day_events:
            day_tex += "{\\fontsize{24}{34}\\selectfont \\textcolor{emphasistext}{ %s }}\\\\\\vspace{0.05cm}\\\\{\\fontsize{20}{30}\\selectfont %s at %s} \\\\" % (day_event['what'], day_event['where'], day_event['when'])
            if day_events.index(day_event) < len(day_events) - 1:
                day_tex += "\\vspace{0.3cm}\\\\"
        day_tex += "\\end{addmargin}\\end{minipage}\\vspace{0.75cm}\n"
        event_content += day_tex

    if len(event_content) > 0:
        event_content += "\\\\" # Only add empty line when there is an event to prevent no line to end error.
    latex_formatting['event_content'] = event_content

    if len(special_text_lines) > 0:
        special_content = "\\begin{minipage}{0.45\\textwidth}{\\fontsize{30}{40}\\selectfont %s }\\\\\\begin{addmargin}[1em]{0em}" % (utils.tex_escape(special_text_lines[0]))
        for line in special_text_lines[1:]:
            special_content += "{\\fontsize{16}{20}\\selectfont %s \\par}" % (utils.tex_escape(line))
        special_content += "\\end{addmargin}\\end{minipage}\\\\"
    latex_formatting['special_text'] = special_content
    latex_template = latex_template % latex_formatting

    # Write PDF, finish.
    print("Writing completed LaTeX to PDF...")
    latex_target_path = utils.get_project_full_path() + "/tex/Constantine.tex"
    with open(latex_target_path, 'w+') as latex_file:
        latex_file.write(latex_template)

    print("Generating PDF...")
    working_dir = utils.get_project_full_path() + "/tex"
    p = subprocess.Popen(['xelatex', latex_target_path], stdout=subprocess.PIPE, cwd=working_dir)
    success = False
    try:
        output = p.communicate(timeout=XELATEX_TIMEOUT)
        result_code = p.returncode

        if result_code == 0:
            success = True
            print("Success! PDF saved at: " + latex_target_path[:-4] + ".pdf")
        else:
            print("Failure! Check " + latex_target_path[:-4] + ".log for details.")
    except subprocess.TimeoutExpired:
        print("Failure! Something has made XeLaTeX to wait. Check " + latex_target_path[:-4] + ".log for details.")

    if not success:
        sys.exit(1)

    print("Copying PDF to " + output_file)
    p = subprocess.Popen(['cp', latex_target_path[:-4] + ".pdf", output_file], stdout=subprocess.PIPE, cwd=os.getcwd())
    result_code = p.returncode
    print("PDF should have been copied to: " + output_file)

if __name__ == '__main__':
    run(sys.argv)
