"""Python wrappers around Brain.

This file is MACHINE GENERATED! Do not edit.
"""

import collections as _collections

from google.protobuf import text_format as _text_format

from tensorflow.core.framework import op_def_pb2 as _op_def_pb2

# Needed to trigger the call to _set_call_cpp_shape_fn.
from tensorflow.python.framework import common_shapes as _common_shapes

from tensorflow.python.framework import op_def_registry as _op_def_registry
from tensorflow.python.framework import ops as _ops
from tensorflow.python.framework import op_def_library as _op_def_library
_bulk_advance_from_oracle_outputs = ["output_handle", "gold_labels"]


_BulkAdvanceFromOracleOutput = _collections.namedtuple("BulkAdvanceFromOracle",
                                                       _bulk_advance_from_oracle_outputs)


def bulk_advance_from_oracle(handle, component, name=None):
  r"""Given a ComputeSession, advances until all states are final.

  Note that, unlike AdvanceFromOracle, this op does mutate the master state, by
  advancing all of its states until they are final.

  Args:
    handle: A `Tensor` of type `string`. A handle to a ComputeSession.
    component: A `string`.
      The name of a Component instance, matching the ComponentSpec.name.
    name: A name for the operation (optional).

  Returns:
    A tuple of `Tensor` objects (output_handle, gold_labels).
    output_handle: A `Tensor` of type `string`. A handle to the same ComputeSession, after it has advanced.
    gold_labels: A `Tensor` of type `int32`. [batch_size * beam_size * max_num_steps] vector of oracle actions,
      where max_num_steps is the maximum number of steps in the oracle
      action sequences for every state in the batch of beams.  Each
      sub-segment of length max_num_steps provides the oracle action
      sequence for the corresponding state in the batch of beams, padded
      with trailing -1s.
  """
  result = _op_def_lib.apply_op("BulkAdvanceFromOracle", handle=handle,
                                component=component, name=name)
  return _BulkAdvanceFromOracleOutput._make(result)


_ops.RegisterShape("BulkAdvanceFromOracle")(None)
_bulk_advance_from_prediction_outputs = ["output_handle"]


def bulk_advance_from_prediction(handle, scores, component, name=None):
  r"""Given a ComputeSession and a tensor of scores, advances the state.

  The state will be advanced until all scores are used up or all states are final.

  Args:
    handle: A `Tensor` of type `string`. A handle to a ComputeSession.
    scores: A `Tensor`. A tensor of scores with shape
      {batch_size * beam_size * num_steps, num_actions}.
    component: A `string`.
      The name of a Component instance, matching the ComponentSpec.name.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `string`.
    handle to the same ComputeSession after advancement.
  """
  result = _op_def_lib.apply_op("BulkAdvanceFromPrediction", handle=handle,
                                scores=scores, component=component, name=name)
  return result


_ops.RegisterShape("BulkAdvanceFromPrediction")(None)
_bulk_fixed_embeddings_outputs = ["output_handle", "embedding_vectors",
                                 "num_steps"]


_BulkFixedEmbeddingsOutput = _collections.namedtuple("BulkFixedEmbeddings",
                                                     _bulk_fixed_embeddings_outputs)


def bulk_fixed_embeddings(handle, embedding_matrix, component,
                          pad_to_batch=None, pad_to_steps=None, name=None):
  r"""This op is a more efficient version of BulkFixedFeatures.

  It is intended to be run with large batch sizes at inference time. The op takes
  a handle to ComputeSession and embedding matrices as tensor inputs, and directly
  outputs concatenated embedding vectors.

  Args:
    handle: A `Tensor` of type `string`. A handle to ComputeSession.
    embedding_matrix: A list of at least 1 `Tensor` objects of the same type.
      Embedding matrices.
    component: A `string`.
      The name of a Component instance, matching the ComponentSpec.name.
    pad_to_batch: An optional `int`. Defaults to `-1`.
      If set, the op will pad/truncate to this number of elements.
    pad_to_steps: An optional `int`. Defaults to `-1`.
      If set, the op will pad/truncate to this number of steps.
    name: A name for the operation (optional).

  Returns:
    A tuple of `Tensor` objects (output_handle, embedding_vectors, num_steps).
    output_handle: A `Tensor` of type `string`. A handle to the same ComputeSession after advancement.
    embedding_vectors: A `Tensor`. Has the same type as `embedding_matrix`. (matrix of float) Concatenated embeddings,
      shaped as (batch * beam * token) x sum_channel(embedding_dim[channel]).
    num_steps: A `Tensor` of type `int32`. The batch was unrolled for these many steps.
  """
  result = _op_def_lib.apply_op("BulkFixedEmbeddings", handle=handle,
                                embedding_matrix=embedding_matrix,
                                component=component,
                                pad_to_batch=pad_to_batch,
                                pad_to_steps=pad_to_steps, name=name)
  return _BulkFixedEmbeddingsOutput._make(result)


_ops.RegisterShape("BulkFixedEmbeddings")(None)
_bulk_fixed_features_outputs = ["output_handle", "indices", "ids", "weights",
                               "num_steps"]


_BulkFixedFeaturesOutput = _collections.namedtuple("BulkFixedFeatures",
                                                   _bulk_fixed_features_outputs)


def bulk_fixed_features(handle, component, num_channels, name=None):
  r"""Given a ComputeSession and a component, outputs fixed features for all steps.

  This op outputs features for the entire oracle path of the component. Unlike
  ExtractFixedFeatures, this op mutates the master state, advancing all of its
  states until they are final. For every channel, indices[channel], ids[channel],
  and weights[channel] have the same length, ie. the number of predicates,
  ordered by batch, beam, step.

  Args:
    handle: A `Tensor` of type `string`. A handle to a ComputeSession.
    component: A `string`.
      The name of a Component instance, matching the ComponentSpec.name.
    num_channels: An `int` that is `>= 1`.
      The number of FixedFeature channels.
    name: A name for the operation (optional).

  Returns:
    A tuple of `Tensor` objects (output_handle, indices, ids, weights, num_steps).
    output_handle: A `Tensor` of type `string`. A handle to the same ComputeSession after advancement.
    indices: A list of `num_channels` `Tensor` objects of type `int32`. (num_channels vectors of int32) If indices[i] = j, then
      embedding_sum[j] += embedding_matrix[ids[i]] * weights[i].
    ids: A list of `num_channels` `Tensor` objects of type `int64`. (num_channels vectors of int64) Ids to lookup in embedding matrices.
    weights: A list of `num_channels` `Tensor` objects of type `float32`. (num_channels vectors of float) Weight for each embedding.
    num_steps: A `Tensor` of type `int32`. (int32 scalar) The batch was unrolled for this many steps.
  """
  result = _op_def_lib.apply_op("BulkFixedFeatures", handle=handle,
                                component=component,
                                num_channels=num_channels, name=name)
  return _BulkFixedFeaturesOutput._make(result)


_ops.RegisterShape("BulkFixedFeatures")(None)
def _InitOpDefLibrary():
  op_list = _op_def_pb2.OpList()
  _text_format.Merge(_InitOpDefLibrary.op_list_ascii, op_list)
  _op_def_registry.register_op_list(op_list)
  op_def_lib = _op_def_library.OpDefLibrary()
  op_def_lib.add_op_list(op_list)
  return op_def_lib


_InitOpDefLibrary.op_list_ascii = """op {
  name: "BulkAdvanceFromOracle"
  input_arg {
    name: "handle"
    type: DT_STRING
  }
  output_arg {
    name: "output_handle"
    type: DT_STRING
  }
  output_arg {
    name: "gold_labels"
    type: DT_INT32
  }
  attr {
    name: "component"
    type: "string"
  }
}
op {
  name: "BulkAdvanceFromPrediction"
  input_arg {
    name: "handle"
    type: DT_STRING
  }
  input_arg {
    name: "scores"
    type_attr: "T"
  }
  output_arg {
    name: "output_handle"
    type: DT_STRING
  }
  attr {
    name: "component"
    type: "string"
  }
  attr {
    name: "T"
    type: "type"
  }
}
op {
  name: "BulkFixedEmbeddings"
  input_arg {
    name: "handle"
    type: DT_STRING
  }
  input_arg {
    name: "embedding_matrix"
    type_attr: "T"
    number_attr: "num_channels"
  }
  output_arg {
    name: "output_handle"
    type: DT_STRING
  }
  output_arg {
    name: "embedding_vectors"
    type_attr: "T"
  }
  output_arg {
    name: "num_steps"
    type: DT_INT32
  }
  attr {
    name: "component"
    type: "string"
  }
  attr {
    name: "num_channels"
    type: "int"
    has_minimum: true
    minimum: 1
  }
  attr {
    name: "T"
    type: "type"
  }
  attr {
    name: "pad_to_batch"
    type: "int"
    default_value {
      i: -1
    }
  }
  attr {
    name: "pad_to_steps"
    type: "int"
    default_value {
      i: -1
    }
  }
  is_stateful: true
}
op {
  name: "BulkFixedFeatures"
  input_arg {
    name: "handle"
    type: DT_STRING
  }
  output_arg {
    name: "output_handle"
    type: DT_STRING
  }
  output_arg {
    name: "indices"
    type: DT_INT32
    number_attr: "num_channels"
  }
  output_arg {
    name: "ids"
    type: DT_INT64
    number_attr: "num_channels"
  }
  output_arg {
    name: "weights"
    type: DT_FLOAT
    number_attr: "num_channels"
  }
  output_arg {
    name: "num_steps"
    type: DT_INT32
  }
  attr {
    name: "component"
    type: "string"
  }
  attr {
    name: "num_channels"
    type: "int"
    has_minimum: true
    minimum: 1
  }
}
"""


_op_def_lib = _InitOpDefLibrary()
