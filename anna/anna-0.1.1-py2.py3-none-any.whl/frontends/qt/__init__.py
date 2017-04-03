# -*- coding: utf-8 -*-

from .forms import ParameterForm

from .parameters import BoolInput, IntegerInput, StringInput, NumberInput, VectorInput, \
    DupletInput, TripletInput, PhysicalQuantityInput, PhysicalVectorQuantityInput, \
    PhysicalDupletInput, PhysicalTripletInput, GroupInput

from .views import ParametrizedComponentView
