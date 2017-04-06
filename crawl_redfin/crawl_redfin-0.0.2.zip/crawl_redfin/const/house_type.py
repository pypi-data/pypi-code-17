#!/usr/bin/env python
# -*- coding: utf-8 -*-

from constant import Constant


class HouseType(Constant):
    class SingleHouse(Constant):
        id = 1
        name = "Single House"
    
    class Condo(Constant):
        id = 2
        name = "Condo"
        
    class TownHouse(Constant):
        id = 3
        name = "Town House"

    class MultiFamily(Constant):
        id = 4
        name = "Multi Family"
        
    class Land(Constant):
        id = 5
        name = "Multi Family"
        
    class OtherType(Constant):
        id = 6
        name = "Other Type"