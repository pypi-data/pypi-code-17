import grpc
from grpc.framework.common import cardinality
from grpc.framework.interfaces.face import utilities as face_utilities

import qbit_pb2 as qbit__pb2
import qbit_pb2 as qbit__pb2
import qbit_pb2 as qbit__pb2
import qbit_pb2 as qbit__pb2
import qbit_pb2 as qbit__pb2
import qbit_pb2 as qbit__pb2
import qbit_pb2 as qbit__pb2
import qbit_pb2 as qbit__pb2
import qbit_pb2 as qbit__pb2
import qbit_pb2 as qbit__pb2
import qbit_pb2 as qbit__pb2
import qbit_pb2 as qbit__pb2
import qbit_pb2 as qbit__pb2
import qbit_pb2 as qbit__pb2
import qbit_pb2 as qbit__pb2
import qbit_pb2 as qbit__pb2
import qbit_pb2 as qbit__pb2
import qbit_pb2 as qbit__pb2
import qbit_pb2 as qbit__pb2
import google.protobuf.empty_pb2 as google_dot_protobuf_dot_empty__pb2


class QuboStub(object):

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.SQA = channel.stream_unary(
        '/qbit.services.Qubo/SQA',
        request_serializer=qbit__pb2.QuadraticRequest.SerializeToString,
        response_deserializer=qbit__pb2.QuadraticResponse.FromString,
        )
    self.Tabu = channel.stream_unary(
        '/qbit.services.Qubo/Tabu',
        request_serializer=qbit__pb2.QuadraticRequest.SerializeToString,
        response_deserializer=qbit__pb2.QuadraticResponse.FromString,
        )


class QuboServicer(object):

  def SQA(self, request_iterator, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Tabu(self, request_iterator, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_QuboServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'SQA': grpc.stream_unary_rpc_method_handler(
          servicer.SQA,
          request_deserializer=qbit__pb2.QuadraticRequest.FromString,
          response_serializer=qbit__pb2.QuadraticResponse.SerializeToString,
      ),
      'Tabu': grpc.stream_unary_rpc_method_handler(
          servicer.Tabu,
          request_deserializer=qbit__pb2.QuadraticRequest.FromString,
          response_serializer=qbit__pb2.QuadraticResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'qbit.services.Qubo', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))


class MolecularSimilarityStub(object):

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Compare = channel.unary_unary(
        '/qbit.services.MolecularSimilarity/Compare',
        request_serializer=qbit__pb2.CompareRequest.SerializeToString,
        response_deserializer=qbit__pb2.ComparisonResult.FromString,
        )


class MolecularSimilarityServicer(object):

  def Compare(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_MolecularSimilarityServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Compare': grpc.unary_unary_rpc_method_handler(
          servicer.Compare,
          request_deserializer=qbit__pb2.CompareRequest.FromString,
          response_serializer=qbit__pb2.ComparisonResult.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'qbit.services.MolecularSimilarity', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))


class MathStub(object):

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Add = channel.unary_unary(
        '/qbit.services.Math/Add',
        request_serializer=qbit__pb2.MathRequest.SerializeToString,
        response_deserializer=qbit__pb2.MathResponse.FromString,
        )
    self.Sub = channel.unary_unary(
        '/qbit.services.Math/Sub',
        request_serializer=qbit__pb2.MathRequest.SerializeToString,
        response_deserializer=qbit__pb2.MathResponse.FromString,
        )


class MathServicer(object):

  def Add(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Sub(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_MathServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Add': grpc.unary_unary_rpc_method_handler(
          servicer.Add,
          request_deserializer=qbit__pb2.MathRequest.FromString,
          response_serializer=qbit__pb2.MathResponse.SerializeToString,
      ),
      'Sub': grpc.unary_unary_rpc_method_handler(
          servicer.Sub,
          request_deserializer=qbit__pb2.MathRequest.FromString,
          response_serializer=qbit__pb2.MathResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'qbit.services.Math', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))


class QbcbcStub(object):

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Quadprog = channel.unary_unary(
        '/qbit.services.Qbcbc/Quadprog',
        request_serializer=qbit__pb2.QuadprogRequest.SerializeToString,
        response_deserializer=qbit__pb2.QuadprogResponse.FromString,
        )
    self.AsyncQuadprog = channel.unary_unary(
        '/qbit.services.Qbcbc/AsyncQuadprog',
        request_serializer=qbit__pb2.QuadprogRequest.SerializeToString,
        response_deserializer=qbit__pb2.Operation.FromString,
        )


class QbcbcServicer(object):

  def Quadprog(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def AsyncQuadprog(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_QbcbcServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Quadprog': grpc.unary_unary_rpc_method_handler(
          servicer.Quadprog,
          request_deserializer=qbit__pb2.QuadprogRequest.FromString,
          response_serializer=qbit__pb2.QuadprogResponse.SerializeToString,
      ),
      'AsyncQuadprog': grpc.unary_unary_rpc_method_handler(
          servicer.AsyncQuadprog,
          request_deserializer=qbit__pb2.QuadprogRequest.FromString,
          response_serializer=qbit__pb2.Operation.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'qbit.services.Qbcbc', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))


class OperationsStub(object):

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.ListOperations = channel.unary_unary(
        '/qbit.services.Operations/ListOperations',
        request_serializer=qbit__pb2.ListOperationsRequest.SerializeToString,
        response_deserializer=qbit__pb2.ListOperationsResponse.FromString,
        )
    self.GetOperation = channel.unary_unary(
        '/qbit.services.Operations/GetOperation',
        request_serializer=qbit__pb2.GetOperationRequest.SerializeToString,
        response_deserializer=qbit__pb2.Operation.FromString,
        )
    self.CancelOperation = channel.unary_unary(
        '/qbit.services.Operations/CancelOperation',
        request_serializer=qbit__pb2.CancelOperationRequest.SerializeToString,
        response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )


class OperationsServicer(object):

  def ListOperations(self, request, context):
    """Lists operations that match the specified filter in the request. If the
    server doesn't support this method, it returns `UNIMPLEMENTED`.

    NOTE: the `name` binding below allows API services to override the binding
    to use different resource name schemes, such as `users/*/operations`.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetOperation(self, request, context):
    """Gets the latest state of a long-running operation.  Clients can use this
    method to poll the operation result at intervals as recommended by the API
    service.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def CancelOperation(self, request, context):
    """Deletes a long-running operation. This method indicates that the client is
    no longer interested in the operation result. It does not cancel the
    operation. If the server doesn't support this method, it returns
    `google.rpc.Code.UNIMPLEMENTED`.
    rpc DeleteOperation(DeleteOperationRequest) returns (google.protobuf.Empty) {}

    Starts asynchronous cancellation on a long-running operation.  The server
    makes a best effort to cancel the operation, but success is not
    guaranteed.  If the server doesn't support this method, it returns
    `google.rpc.Code.UNIMPLEMENTED`.  Clients can use
    [Operations.GetOperation][google.longrunning.Operations.GetOperation] or
    other methods to check whether the cancellation succeeded or whether the
    operation completed despite cancellation. On successful cancellation,
    the operation is not deleted; instead, it becomes an operation with
    an [Operation.error][google.longrunning.Operation.error] value with a [google.rpc.Status.code][google.rpc.Status.code] of 1,
    corresponding to `Code.CANCELLED`.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_OperationsServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'ListOperations': grpc.unary_unary_rpc_method_handler(
          servicer.ListOperations,
          request_deserializer=qbit__pb2.ListOperationsRequest.FromString,
          response_serializer=qbit__pb2.ListOperationsResponse.SerializeToString,
      ),
      'GetOperation': grpc.unary_unary_rpc_method_handler(
          servicer.GetOperation,
          request_deserializer=qbit__pb2.GetOperationRequest.FromString,
          response_serializer=qbit__pb2.Operation.SerializeToString,
      ),
      'CancelOperation': grpc.unary_unary_rpc_method_handler(
          servicer.CancelOperation,
          request_deserializer=qbit__pb2.CancelOperationRequest.FromString,
          response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'qbit.services.Operations', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
