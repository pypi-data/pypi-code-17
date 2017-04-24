#!/bin/python
import roomai
import random
from roomai.doudizhu.DouDiZhuPokerUtils import *

class DouDiZhuPokerRandomPlayer(roomai.abstract.AbstractPlayer):
    
    def __init__(self):
        self.id1                = None
        self.hand_cards         = None
        self.public_state       = None
        self.available_actions  = None
    
    #@override    
    def receive_info(self, info):
        if info.init_id is not None:
            self.id1 = info.init_id
        if info.init_cards is not None:
            self.hand_cards = info.init_cards
        if info.init_addcards is not None  and info.public_state.landlord_id == self.id1:
            self.hand_cards.add_cards(info.init_addcards)

        if info.available_actions is not None:
            self.available_actions = info.available_actions

        self.public_state = info.public_state

    #@override
    def take_action(self):
        candidates = self.available_actions.values()
        idx = int(random.random() * len(candidates))
        action = candidates[idx]
        self.hand_cards.remove_action(action)
        return action


    #@override
    def reset(self, action):
        self.id1            = None
        self.hand_cards     = None
        self.public_state   = None
