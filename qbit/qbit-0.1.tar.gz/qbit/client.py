import grpc
import json
import time
import requests
import qbit_pb2

from google.protobuf.struct_pb2 import Struct
from google.protobuf.json_format import MessageToDict

def create_get_auth(access_token):
    def get_auth_token(context, callback):
        callback([('authorization', access_token)], None)
    return get_auth_token

def generate_quadratic(q2d):
    for q1d in q2d:
        qr = qbit_pb2.QuadraticRequest()
        for var in q1d:
            qr.quadraticArray.append(var)
        yield qr

def list_to_fl(matrix):
    out = []
    for row in matrix:
        out.append(qbit_pb2.QuadprogRequest.float_list(items=row))
    return out

def shares_to_list(res):
    out = []
    for row in res.shares:
        out.append(row)
    return out

def kwargs_to_quadprog(kwargs):
    qr = qbit_pb2.QuadprogRequest()

    for key, value in kwargs.iteritems():
        if(key == 'lin_obj_vec'):
            qr.lin_obj_vec.extend(value)
        elif(key == 'quad_obj_mat'):
            qr.quad_obj_mat.extend(list_to_fl(value))
        elif(key == 'lb'):
            qr.lb.extend(value)
        elif(key == 'ub'):
            qr.ub.extend(value)
        elif(key == 'ineq_con_mat'):
            qr.ineq_con_mat.extend(list_to_fl(value))
        elif(key == 'ineq_con_vec'):
            qr.ineq_con_vec.extend(value)
        elif(key == 'eq_con_mat'):
            qr.eq_con_mat.extend(list_to_fl(value))
        elif(key == 'eq_con_vec'):
            qr.eq_con_vec.extend(value)
        elif(key == 'is_min'):
            qr.lpProblem = 0 if value else 1
        elif(key == 'multiplier'):
            qr.multiplier = value
        elif(key == 'verbose'):
            qr.verbose = value
        elif(key == 'lp_file_name'):
            qr.lp_file_name = value
        elif(key == 'threads'):
            qr.threads = value
        elif(key == 'presolve'):
            qr.presolve = value
        elif(key == 'cuts'):
            qr.presolve = value
        elif(key == 'dual'):
            qr.dual = value
        elif(key == 'strong'):
            qr.strong = value
        elif(key == 'max_seconds'):
            qr.max_seconds = value

    return qr


# Client class takes care of authentication process in order to use our services
#
# Example -
# from qbit import client
# solution = client('./qbit/license.json').math_add(2,5)
class grpc_channel(object):
    def __init__(self, license=None,
        client_id=None, client_secret=None, root_certs=None,
        private_key=None, cert_chain=None,
        url=None):
        if not license and (not client_id or not client_secret or
                not root_certs or not private_key or not cert_chain):
            raise Exception("Please provide either license file or " +
                "all of client_id, client_secret, root_certs, " +
                "private_key and cert_chain")

        if license:
            with open(license) as data_file:
                data = json.load(data_file)
            client_id = data["client_id"]
            client_secret = data["client_secret"]
            root_certs = data["root_certs"].encode('utf8')
            private_key = data["private_key"].encode('utf8')
            cert_chain = data["cert_chain"].encode('utf8')
        else:
            client_id = client_id
            client_secret = client_secret
            root_certs = root_certs.encode('utf8')
            private_key = private_key.encode('utf8')
            cert_chain = cert_chain.encode('utf8')

        url = url if url else "https://1qbit.auth0.com/oauth/token"

        req_dict = {"client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials",
            "audience": "http://api.1qb.it"}
        try:
            response = requests.post(url, json=req_dict).json()
        except Exception as e:
            raise Exception("Request has Failed: ", e.message)

        if response.has_key("error"):
            if response.has_key("error_description"):
                raise Exception(response["error"], ": ",
                    response["error_description"])
            raise Exception(response)
        elif response.has_key("access_token"):
            token = response["access_token"]

        transport_creds = grpc.ssl_channel_credentials(root_certs,
            private_key, cert_chain)
        auth_creds = grpc.metadata_call_credentials(create_get_auth(token))
        channel_creds = grpc.composite_channel_credentials(transport_creds, auth_creds)
        self._channel = grpc.secure_channel('grpc.1qb.it', channel_creds)

class client(grpc_channel):
    def __init__(self, license=None,
        client_id=None, client_secret=None, root_certs=None,
        private_key=None, cert_chain=None,
        url=None):

        super(client, self).__init__(license, client_id, client_secret, root_certs,
            private_key, cert_chain, url)

        self.mathStub = qbit_pb2.MathStub(self._channel)
        self.quboStub = qbit_pb2.QuboStub(self._channel)
        self.msStub = qbit_pb2.MolecularSimilarityStub(self._channel)
        self.qbcbcStub = qbit_pb2.QbcbcStub(self._channel)
        self.operationStub = qbit_pb2.OperationsStub(self._channel)

    def math_add(self, a, b):
        return self.mathStub.Add(qbit_pb2.MathRequest(a=a,b=b))

    def math_sub(self, a, b):
        return self.mathStub.Sub(qbit_pb2.MathRequest(a=a,b=b))

    def ms_compare(self, smiles, solver_type, should_visualize):
        return self.msStub.Compare(qbit_pb2.CompareRequest(
            smiles=smiles, solver_type=solver_type, should_visualize=should_visualize))

    def qubo_tabu(self, matrix):
        quadratic_sqa = generate_quadratic(matrix)
        return self.quboStub.Tabu(quadratic_sqa)

    def qubo_sqa(self, matrix):
        quadratic_sqa = generate_quadratic(matrix)
        return self.quboStub.SQA(quadratic_sqa)

    def qbcbc_quadprog(self, **kwargs):
        """List of Keyword arguments(Keyword: Type)
lin_obj_vec: Array of Double
quad_obj_mat: 2D Array of Double
lb: Array of Double
ub: Array of Double
ineq_con_mat: 2D Array of Double
ineq_con_vec: Array of Double
eq_con_mat: 2D Array of Double
eq_con_vec: Array of Double
is_min: Bool
multiplier: Int
verbose: Bool
lp_file_name: String
threads: Bool
presolve: Bool
cuts: Bool
dual: Bool
strong: Bool
max_seconds: Int"""
        return self.qbcbcStub.Quadprog(kwargs_to_quadprog(kwargs))

    def qbcbc_async_quadprog(self, **kwargs):
        """List of Keyword arguments(Keyword: Type)
lin_obj_vec: Array of Double
quad_obj_mat: 2D Array of Double
lb: Array of Double
ub: Array of Double
ineq_con_mat: 2D Array of Double
ineq_con_vec: Array of Double
eq_con_mat: 2D Array of Double
eq_con_vec: Array of Double
is_min: Bool
multiplier: Int
verbose: Bool
lp_file_name: String
threads: Bool
presolve: Bool
cuts: Bool
dual: Bool
strong: Bool
max_seconds: Int"""
        return self.qbcbcStub.AsyncQuadprog(kwargs_to_quadprog(kwargs))

    def operation_get(self, id):
        return self.operationStub.GetOperation(
            qbit_pb2.GetOperationRequest(name=str(id)))

    def operation_cancel(self, id):
        return self.operationStub.CancelOperation(
            qbit_pb2.CancelOperationRequest(name=str(id)))

    def operation_list(self, filter=""):
        return self.operationStub.ListOperations(
            qbit_pb2.ListOperationsRequest(filter=filter))


class quadprog(grpc_channel):
    def __init__(self, license=None,
        client_id=None, client_secret=None, root_certs=None,
        private_key=None, cert_chain=None,
        url=None):

        super(quadprog, self).__init__(license, client_id, client_secret, root_certs,
            private_key, cert_chain, url)

        self.qbcbcStub = qbit_pb2.QbcbcStub(self._channel)
        self.operationStub = qbit_pb2.OperationsStub(self._channel)

        self.quadprog_request = qbit_pb2.QuadprogRequest()

        self.result = None
        self.status = None
        self.name = None

    def set_lin_obj_vec(self, lin_obj_vec):
        self.quadprog_request.ClearField('lin_obj_vec')
        self.quadprog_request.lin_obj_vec.extend(lin_obj_vec)

    def set_quad_obj_mat(self, quad_obj_mat):
        self.quadprog_request.ClearField('quad_obj_mat')
        self.quadprog_request.quad_obj_mat.extend(list_to_fl(quad_obj_mat))

    def set_lb(self, lb):
        self.quadprog_request.ClearField('lb')
        self.quadprog_request.lb.extend(lb)

    def set_ub(self, ub):
        self.quadprog_request.ClearField('ub')
        self.quadprog_request.ub.extend(ub)

    def set_ineq_con_mat(self, ineq_con_mat):
        self.quadprog_request.ClearField('ineq_con_mat')
        self.quadprog_request.ineq_con_mat.extend(list_to_fl(ineq_con_mat))

    def set_ineq_con_vec(self, ineq_con_vec):
        self.quadprog_request.ClearField('ineq_con_vec')
        self.quadprog_request.ineq_con_vec.extend(ineq_con_vec)

    def set_eq_con_mat(self, eq_con_mat):
        self.quadprog_request.ClearField('eq_con_mat')
        self.quadprog_request.eq_con_mat.extend(list_to_fl(eq_con_mat))

    def set_eq_con_vec(self, eq_con_vec):
        self.quadprog_request.ClearField('eq_con_vec')
        self.quadprog_request.eq_con_vec.extend(eq_con_vec)

    def verify(self):
        if (len(self.quadprog_request.lin_obj_vec)==0):
            return False

        if (len(self.quadprog_request.quad_obj_mat)==0):
            return False

        if (len(self.quadprog_request.lb)==0):
            return False

        if (len(self.quadprog_request.ub)==0):
            return False

        if (len(self.quadprog_request.ineq_con_mat)==0):
            print 'warning: ineq_con_mat is not set'

        if (len(self.quadprog_request.ineq_con_vec)==0):
            print 'warning: ineq_con_vec is not set'

        if (len(self.quadprog_request.eq_con_mat)==0):
            print 'warning: eq_con_mat is not set'

        if (len(self.quadprog_request.eq_con_vec)==0):
            print 'warning: eq_con_vec is not set'

        return True

    def solve(self):
        if not self.verify():
            return

        if self.status != None:
            print 'This problem is already queued. Please cancel it first'
            return

        print 'Attempting to solve the problem'
        quadprog_response = self.qbcbcStub.Quadprog(self.quadprog_request)
        self.result = shares_to_list(quadprog_response)
        self.status = 'finished'

        return self.result

    def queue(self):
        if not self.verify():
            return

        print 'Queueing the problem'
        response = self.qbcbcStub.AsyncQuadprog(self.quadprog_request)
        self.name = int(response.name)
        self.status = 'pending'

    def cancel_queue(self):
        if self.name == None:
            return

        self.operationStub.CancelOperation(
            qbit_pb2.CancelOperationRequest(name=str(self.name)))
        self.name = None
        self.status = None

    def update_status(self):
        """Updates the status('pending', 'running', 'finished') variable of this object.
If status is finished or doesn't exist in queue, it will update the result variable and return true.
Otherwise, it returns false.
        """
        if self.name == None:
            print 'This problem is not queued'
            return True

        response = self.operationStub.GetOperation(
            qbit_pb2.GetOperationRequest(name=str(self.name)))
        res_dict = MessageToDict(response)

        self.status = str(res_dict.get('metadata').get('value').get('status'))
        
        if not response.done:
            return False

        if res_dict.has_key('response'):
            self.result = res_dict.get('response').get('shares')
            return True

        if res_dict.has_key('error'):
            self.result = res_dict.get('error').get('message')
            return True

    def wait_for_queue_result(self, sleep_time=5):
        while not self.update_status():
            time.sleep(sleep_time)
