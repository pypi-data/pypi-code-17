

def info(args, server):
    job = server.get_job_info(args.job)
    # print(job)
    default_args = []

    name = job["displayName"]
    status = job['color']
    url = job['url']

    print("Name:{}".format(name))
    print("Status:{}".format(status))
    print("URL:{}".format(url))
    # Parameters
    job_actions = job['actions']

    print("\nJob Parameters\n")
    for action in job_actions:
        try:
            if action['_class'] == 'hudson.model.ParametersDefinitionProperty':
                definitions = action['parameterDefinitions']
                for param in definitions:
                    param_name = param['name']
                    param_value = param['defaultParameterValue']['value']
                    if param_value:
                        default_args.append("{}={}".format(param_name, param_value))

                    print("Name:{} Default: {}".format(param_name, param_value))
        except KeyError:
            pass

    # wrap Run command
    cmd = "jenkins run {} {}".format(name, ' '.join(default_args))
    print("\nTo trigger this job execute:\n")
    print(cmd)