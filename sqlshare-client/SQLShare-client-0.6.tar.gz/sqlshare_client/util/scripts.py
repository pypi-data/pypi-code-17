from sqlshare_client import Client
from sqlshare_client.util.command_line import get_oauth_values
from tabulate import tabulate
import sys
import re

MAX_QUERY_DISPLAY = 80


def get_client(parser=None):
    data = get_oauth_values(parser)

    if 'id' not in data:
        print "Error: You need to specify a credentials path."
        raise Exception("Unconfigured")

    client = Client(oauth_id=data['id'],
                    oauth_secret=data['secret'],
                    server=data['server'],
                    redirect_uri=data['redirect_uri'],
                    grant_type=data.get('grant_type', None))

    if not client.has_access():
        print "You need to give this application access to your data."
        print "Visit the URL below to continue, and then enter the code below."
        print client.get_authorize_url()

        code = sys.stdin.readline()[:-1]
        client.get_tokens_for_code(code=code)

    return client


def list_datasets(datasets):
    for ds in sorted(datasets):
        print "%s/%s - %s" % (ds.owner, ds.name, ds.url)


def dump_dataset(dataset):
    for key in sorted(dir(dataset)):
        if not key.startswith('__'):
            print "%s: %s" % (key, getattr(dataset, key))


def display_query(query):
    if query.error:
        print "Error running query: %s" % (query.error)
        return

    print tabulate(query.sample_data, headers=query.columns)


def display_query_list(query_list):
    data = []
    headers = ["ID", "Date Started", "Date Finished", "Status", "SQL"]

    for query in query_list:
        qid = re.match('.*?([\d]+$)', query.url).groups()[0]
        sql = query.sql_code
        if sql is None:
            sql = ""

        sql = sql.replace("\n", "\\n")
        if len(sql) > MAX_QUERY_DISPLAY:
            sql = sql[:MAX_QUERY_DISPLAY]
            sql += "..."
        data.append([qid,
                     query.date_created,
                     query.date_finished,
                     query.sample_data_status,
                     sql
                     ])

    print tabulate(data, headers=headers)


def print_to_file(handle, query):
    handle.write(",".join(query.columns))
    handle.write("\n")

    for row in query.sample_data:
        handle.write(",".join(map(lambda x: "%s" % x, row)))
        handle.write("\n")
