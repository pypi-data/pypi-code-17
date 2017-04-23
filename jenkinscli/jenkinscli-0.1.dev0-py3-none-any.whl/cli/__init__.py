import ssl
import os

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

home = os.path.expanduser('~')

jenkins_file = os.getenv("JENKINS_FILE")

if jenkins_file is None:
    jenkins_file = "{}/.jenkins_config.yml".format(home)

try:
    with open(jenkins_file) as infile:
        jenkins_url = infile.readline()[:-1]
        username = infile.readline()[:-1]
        password = infile.readline()[:-1]
        DEFAULT_CONFIG = (jenkins_url, username, password)
except:
    # This is our first try to collect configuration
    pass