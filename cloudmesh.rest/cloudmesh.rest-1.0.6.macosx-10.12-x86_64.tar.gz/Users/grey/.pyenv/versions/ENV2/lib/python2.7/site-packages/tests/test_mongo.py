""" run with

python setup.py install; nosetests -v --nocapture tests/test_mongo.py:Test_mongo.test_001

nosetests -v --nocapture tests/test_mongo.py

or

nosetests -v tests/cm_basic/test_shell.py

"""
from __future__ import print_function

from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.util import HEADING

from cloudmesh.rest.server.mongo import Mongo

def run(command):
    parameter = command.split(" ")
    shell_command = parameter[0]
    args = parameter[1:]
    result = Shell.execute(shell_command, args)
    return str(result)


# noinspection PyMethodMayBeStatic,PyPep8Naming
class Test_mongo(object):
    """

    """

    def setup(self):
        pass

    def test_001(self):
        HEADING("start mongo")

        mongo = Mongo()
        r = mongo.start()
        print(r)
        r = mongo.status()
        print (r)

        assert False
