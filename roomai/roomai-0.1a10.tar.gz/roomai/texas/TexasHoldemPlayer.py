#!/bin/python
#coding:utf-8
import random
import roomai.abstract
from roomai.kuhn import *

class TexasHoldemRandomPlayer(roomai.abstract.AbstractPlayer):
    def __init__(self):
        self.available_actions = None
           
    def receive_info(self, info):
        self.available_actions = info.available_actions

    def take_action(self):
        idx  = int(random.random() * len(self.available_actions))
        keys = self.available_actions.keys()
        return self.available_actions[keys[idx]]

    def reset(self):
        pass
