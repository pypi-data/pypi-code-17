#!/bin/python
#coding:utf-8
import random
import roomai.abstract
from roomai.kuhn import *

class KuhnPokerAlwaysBetPlayer(roomai.abstract.AbstractPlayer):
    def __init__(self):
        pass
           
    def receive_info(self, info):
        pass     

    def take_action(self):
        return ActionSpace.bet

    def reset(self):
        pass
