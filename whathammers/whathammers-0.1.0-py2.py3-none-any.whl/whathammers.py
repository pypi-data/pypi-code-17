import argparse
import re
import sys

from apache_log_parser import (
    make_parser, ApacheLogParserException, LineDoesntMatchException
)
from .reports import (
    top_values_by_hits, top_values_by_total_time,
    top_values_by_time_per_hit, hits_by_slice,
    time_by_slice, time_per_hit_by_slice
)
from .utils import field_description, is_continuous


def get_args():
    parser = argparse.ArgumentParser(
        description="Apache httpd log file analyzer"
    )
    parser.add_argument(
        "logfile",
        help="Path to one or more Apache httpd log file. If none is " +
             "present this will read from stdin",
        nargs="*",
        type=argparse.FileType('r'),
        default=[sys.stdin]
    )
    parser.add_argument(
        "-f", "--format",
        help="Format of the Apache httpd logfile, using the Apache logfile " +
             " format. Default is the Apache Common Log Format, or " +
             "'%%h %%l %%u %%t \"%%r\" %%>s %%b'. You should use the format " +
             "defined  for your server/vhost under the LogFormat " +
             "directive.",
        default="%h %l %u %t \"%r\" %>s %b"
    )
    parser.add_argument(
        "-r", "--reports",
        help="Reports to generate. This is a comma separated list of " +
             " <fieldname>:[h|t|b]. For discrete fields adding 'h' " +
             " will show the top N values of <fieldname> by number of " +
             " hits; 't' by total time and 'b' by time per hit. For " +
             " continuous fields (only time_received is considered " +
             " continuous) this will divide the available range in N " +
             " slices and show the number of hits, total time or time per " +
             " hit for each slice. The list of available fields is output " +
             " at top of the report. Also note that t and b reports are " +
             " only available if request times are logged. Default is " +
             " 'remote_host:ht,request_header_user_agent:ht," +
             "request_url_path:hb,time_received:hb' ",
        default="remote_host:ht,request_header_user_agent:ht," +
                "request_url_path:h,time_received:hb"
    )
    parser.add_argument(
        "-c", "--count",
        help="Number of items to return eg. top 5 IP addresses. Default 5.",
        type=int,
        default=5
    )
    args = parser.parse_args()
    return args


def parse_file(log_file, log_parser):
    parsed = []
    for line in log_file:
        parsed.append(log_parser(line))
    return parsed


def print_field_reports(field_definition, signature, data, count):
    try:
        (field_name, report_list) = field_definition.split(':', 1)
    except ValueError:
        print(("Malformed report value: %s. This should be " +
               "<field_name>:[htb]\n") % field_definition)
        return
    if field_name not in signature:
        print("Field %s not present in log file\n" % field_name)
        return
    if not re.match('^[htb]+$', report_list):
        print("Available reports for %s are h,t and b." % (
            field_name, report_list
        ))
        return

    description = field_description(field_name)

    if 'h' in report_list:
        if is_continuous(field_name):
            report = hits_by_slice(field_name, description, data, count)
        else:
            report = top_values_by_hits(field_name, description, data, count)
        print("\n".join(report)+"\n")
    if 't' in report_list and 'time_us' in signature:
        if is_continuous(field_name):
            report = time_by_slice(field_name, description, data, count)
        else:
            report = top_values_by_total_time(
                field_name, description, data, count
            )
        print("\n".join(report)+"\n")
    if 'b' in report_list and 'time_us' in signature:
        if is_continuous(field_name):
            report = time_per_hit_by_slice(
                field_name, description, data, count
            )
        else:
            report = top_values_by_time_per_hit(
                field_name, description, data, count
            )
        print("\n".join(report)+"\n")


def main():
    args = get_args()
    log_parser = make_parser(args.format)

    print('Parsing files....')
    data = []
    for log_file in args.logfile:
        try:
            data = data + parse_file(log_file, log_parser)
        except LineDoesntMatchException as e:
            sys.exit("Could not parse the following log line: %s" % e.log_line)
        except ApacheLogParserException as e:
            sys.exit(
                "Could not parse file. Internal error message: %s" % str(e)
            )

    signature = data[0].keys()
    print('Logged fields : ' + ', '.join(sorted(signature)))
    print('')

    reports = args.reports.split(',')
    for report_definition in reports:
        print_field_reports(
            report_definition,
            signature,
            data, args.count
        )
