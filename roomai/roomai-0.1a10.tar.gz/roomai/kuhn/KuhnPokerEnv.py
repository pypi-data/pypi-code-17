#!/bin/python
import random
import math
import copy
import roomai.abstract
from KuhnPokerUtils import *;

class KuhnPokerEnv(roomai.abstract.AbstractEnv):

    #@override
    def init(self):

        self.private_state = PrivateState()
        self.public_state  = PublicState()

        card0 = math.floor(random.random() * 3)
        card1 = math.floor(random.random() * 3)
        while card0 == card1:
            card0 = math.floor(random.random() * 3)
        self.private_state.hand_cards = [card0, card1]

        self.public_state.turn          = int(random.random() * 2)
        self.public_state.first         = self.public_state.turn
        self.public_state.epoch         = 0
        self.public_state.action_list   = []
        
        infos = self.gen_infos(2)
        infos[0].player_id = 0
        infos[0].card      = card0
        infos[1].player_id = 1
        infos[1].card      = card1
        
        return False, [], infos 

    #@override
    def forward(self, action):
        self.public_state.epoch += 1
        self.public_state.turn   = (self.public_state.turn+1)%2
        self.public_state.action_list.append(action)
        infos = self.gen_infos(2)


        if self.public_state.epoch == 1:
            return False, [], infos

        elif self.public_state.epoch == 2:
            scores = self.evaluteTwo()
            if scores[0] != -1:
                return True, scores, infos
            else:
                return False,[],infos

        elif self.public_state.epoch == 3:
            scores = self.evaluteThree()
            return True, scores, infos

        else:
            raise Exception("KuhnPoker has 3 turns at most")

    #@Overide
    @classmethod
    def round(cls, env, players):

        isTerminal, scores, infos = env.init()

        for i in xrange(len(players)):
            players[i].receive_info(infos[i])

        while isTerminal == False:
            turn = infos[-1].public_state.turn
            action = players[turn].take_action()
            isTerminal, scores, infos = env.forward(action)
            for i in xrange(len(players)):
                players[i].receive_info(infos[i])

        return scores

    def gen_infos(self,num):
        infos = [Info(), Info(), Info()]
        for i in xrange(num+1):
            infos[i].public_state = copy.deepcopy(self.public_state)
        infos[num].private_state = copy.deepcopy(self.private_state)

        turn = self.public_state.turn
        infos[turn].available_actions = [ActionSpace.cheat, ActionSpace.bet]

        return infos

    def WhoHasHigherCard(self):
        hand_cards = self.private_state.hand_cards
        if hand_cards[0] > hand_cards[1]:
            return 0
        else:
            return 1

    def evaluteTwo(self):
        win    = self.WhoHasHigherCard()
        first  = self.public_state.first
        scores = [0, 0];
        actions = self.public_state.action_list
        
        if actions[0] == ActionSpace.cheat and \
           actions[1] == ActionSpace.bet:
            return [-1,-1]
        
        if actions[0] == actions[1] and \
           actions[0] == ActionSpace.cheat:
            scores[win] = 1;
            return scores;

        if actions[0] == ActionSpace.bet and \
           actions[1] == ActionSpace.cheat:
            scores[first] = 1;
            return scores;

        if actions[0] == actions[1] and \
           actions[0] == ActionSpace.bet:
            scores[win] = 2
            return scores;


    def evaluteThree(self):
        first   = self.public_state.first 
        win     = self.WhoHasHigherCard()
        scores  = [0, 0]
        if self.public_state.action_list[2] == ActionSpace.cheat:
            scores[1 - first] = 1;
        else:
            scores[win] = 2;
        return scores;
       
