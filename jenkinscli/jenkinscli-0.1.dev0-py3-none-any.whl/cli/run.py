import re

def job_arguments_parser(arguments):
    """Parse Jobs argument into a dict like"""
    job_args = {}
    for arg in arguments:
        try:
            key, value = tuple(arg.split('='))
            job_args[key] = value
        except ValueError:
            print("Unknown argument. Should be argument_name=value arg2=value")
            return None

    return job_args


def run(args, server):
    job = args.job
    parameters = None

    if args.arguments:
        parameters = job_arguments_parser(args.arguments)
        if parameters is None:
            return None

    # if args.
    print("Calling job {}".format(job))
    server.build_job(job, parameters=parameters)
    print("Build triggered!")
    # last_build_number = server.get_job_info(job)['lastCompletedBuild']['number']



