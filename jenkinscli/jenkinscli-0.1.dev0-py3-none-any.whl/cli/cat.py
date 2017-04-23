
def get_build_number(server, job_name):
    info = server.get_job_info(job_name)
    if not info['lastBuild']:
        return None
    else:
        build_number = info['lastBuild'].get('number')
    return build_number


def cat(args, server):
    """Collect full console log of last build from given job """
    job_name = args.job

    build_number = get_build_number(server, job_name)
    if build_number is None:
        print("Cannot show console output. %(job_name)s has no builds" % {'job_name': args.job})
        return None

    console_out = server.get_build_console_output(job_name, build_number)
    print(console_out, end='\n')

    # console_out = console_out.split('\n')
    # print("\n".join(console_out))