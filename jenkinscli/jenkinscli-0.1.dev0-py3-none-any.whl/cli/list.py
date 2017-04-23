import re


def list_jobs(args, server):

    jobs = server.get_jobs(folder_depth=None, view_name=args.view)

    for job in jobs:
        if re.search(args.pattern, job['name'], flags=re.I):
            print(job['name'])
