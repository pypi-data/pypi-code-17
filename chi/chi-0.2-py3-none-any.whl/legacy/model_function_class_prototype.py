import traceback
import sys

# def myfun():
#   raise Exception('fdsf')
#
# try:
#   myfun()
# except Exception as e:
#   type, value, tb = sys.exc_info()
#   for filename, line_number, function_name, text in traceback.extract_tb(tb):
#     print(filename)

class m(type):
  print('m')
  def __new__(mcs, *args, **kwargs):
    print('mock', mcs)

  def __init__(cls):
    print(cls)

    cls.bla = 4



class Model:
  __metaclass__ = m

  print('my')
  variables = None

  def __new__(cls, *args, **kwargs):
    print('new', cls, *args)
    return 3

  def __init_subclass__(cls, **kwargs):
    print('init', cls, *kwargs.items())


class Actor (Model):

  def __init__(self, x):
    pass


a = Actor(3)
print(a)

class Function:
  def __new__(mcs, *args, **kwargs):
    print('new', mcs, *args)
    return 3


class train (Function):
  def __init__(self):
    pass

  def run(self):
    pass


import tensorflow as tf
from typing import Type, TypeVar
t = TypeVar('T', bound=tf.Tensor)

def T(dtype=tf.float32, shape=None):
  class TensorAnnotation(tf.Tensor):
    t = dtype
    s = shape
  return TensorAnnotation


def my(g: T(3, 4)):
  pass

from inspect import signature
print(signature(my).parameters['g'].annotation.t)



print(train(5))
# my.__call__ = lambda *args, **kwargs: print(args)
#
#
# a = my()
# a()