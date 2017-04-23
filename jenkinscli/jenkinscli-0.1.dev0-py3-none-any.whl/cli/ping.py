

def ping(args, server):
    data = server.get_whoami()
    version = server.get_version()
    name = data['fullName']

    print("Hello {}, we've connected to Jenkins Server version:{}".format(name, version))