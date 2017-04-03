# -*- coding: utf-8 -*-

import os.path

from .configuration import Configurable, depends_on, document_parameters, parametrize

from .input import Unit, Value

from .parameters import BoolParameter, IntegerParameter, StringParameter, NumberParameter,\
    VectorParameter, DupletParameter, TripletParameter, PhysicalQuantityParameter, \
    ActionParameter, ChoiceParameter, ParameterGroup, VectorParameter, TupleParameter, \
    DupletParameter, TripletParameter

from .adaptors import JSONAdaptor, XMLAdaptor, load_from_file

with open(os.path.join(os.path.split(__file__)[0], 'VERSION')) as fp:
    __version__ = fp.read()


Bool = BoolParameter
Integer = IntegerParameter
String = StringParameter
Number = NumberParameter
PhysicalQuantity = PhysicalQuantityParameter
Action = ActionParameter
Choice = ChoiceParameter
Group = ParameterGroup
Vector = VectorParameter
Tuple = TupleParameter
Duplet = DupletParameter
Triplet = TripletParameter
