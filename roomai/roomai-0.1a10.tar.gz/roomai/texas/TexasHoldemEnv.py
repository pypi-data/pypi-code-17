#!/bin/python
#coding:utf-8

import random
import copy
import roomai.abstract
import roomai
import logging

from TexasHoldemUtil import *


class TexasHoldemEnv(roomai.abstract.AbstractEnv):

    def __init__(self):
        self.logger         = roomai.get_logger()
        self.num_players    = 3 
        self.dealer_id      = int(random.random() * self.num_players)
        self.chips          = [1000 for i in xrange(self.num_players)]
        self.big_blind_bet  = 10

        logger = roomai.get_logger()

    # Before init, you need set the num_players, dealer_id, and chips
    #@override
    def init(self):
        isTerminal = False
        scores     = []

        ## public info
        small = (self.dealer_id + 1) % self.num_players
        big   = (self.dealer_id + 2) % self.num_players

        self.public_state                       = PublicState()
        self.public_state.num_players           = self.num_players
        self.public_state.dealer_id             = self.dealer_id
        self.public_state.big_blind_bet         = self.big_blind_bet
        self.public_state.raise_account         = self.big_blind_bet
        self.public_state.is_quit               = [False for i in xrange(self.num_players)]
        self.public_state.num_quit              = 0
        self.public_state.is_allin              = [False for i in xrange(self.num_players)]
        self.public_state.num_allin             = 0
        self.public_state.bets                  = [0 for i in xrange(self.num_players)]
        self.public_state.chips                 = self.chips
        self.public_state.stage                 = StageSpace.firstStage
        self.public_state.turn                  = self.next_player(big)
        self.public_state.flag_nextstage        = self.next_player(big)
        self.public_state.public_cards          = []

        self.public_state.previous_id           = None
        self.public_state.previous_action       = None

        if self.public_state.chips[big] > self.big_blind_bet:
            self.public_state.chips[big] -= self.big_blind_bet
            self.public_state.bets[big]  += self.big_blind_bet
        else:
            self.public_state.bets[big]     = self.public_state.chips[big]
            self.public_state.chips[big]    = 0
            self.public_state.is_allin[big] = True
            self.public_state.num_allin    += 1
        self.public_state.max_bet       = self.public_state.bets[big]
        self.public_state.raise_account = self.big_blind_bet

        if self.public_state.chips[small] > self.big_blind_bet / 2:
            self.public_state.chips[small] -= self.big_blind_bet /2
            self.public_state.bets[small]  += self.big_blind_bet /2
        else:
            self.public_state.bets[small]     = self.public_state.chips[small]
            self.public_state.chips[small]    = 0
            self.public_state.is_allin[small] = True
            self.public_state.num_allin      += 1

        # private info
        self.private_state = PrivateState() 
        allcards = []
        for i in xrange(13):
            for j in xrange(4):
                allcards.append(Card(i,j))
        random.shuffle(allcards)        
        self.private_state.hand_cards       = [[] for i in xrange(self.num_players)]
        for i in xrange(self.num_players):
            self.private_state.hand_cards[i]    = allcards[i*2:(i+1)*2]
        self.private_state.keep_cards   = allcards[self.num_players*2:self.num_players*2+5]         
        
        #gen info
        infos = [Info() for i in xrange(self.public_state.num_players+1)]
        for i in xrange(len(infos)):
            infos[i].public_state = copy.deepcopy(self.public_state)
        infos[len(infos) - 1].private_state = copy.deepcopy(self.private_state)
        for i in xrange(len(infos)-1):
            infos[i].init_player_id  = i
            infos[i].init_hand_cards = copy.deepcopy(self.private_state.hand_cards[i])
        turn = self.public_state.turn
        infos[turn].available_actions = self.available_actions()

        if self.logger.level <= logging.DEBUG:
            self.logger.debug("TexasHoldemEnv.init: num_players = %d, dealer_id = %d, chip = %d, big_blind_bet = %d"%(\
                self.public_state.num_players,\
                self.public_state.dealer_id,\
                self.public_state.chips[0],\
                self.public_state.big_blind_bet
            ))

        return isTerminal, scores, infos

    ## we need ensure the action is valid
    #@Overide
    def forward(self, action):

        if self.logger.level <= logging.DEBUG:
            self.logger.debug("TexasHoldemEnv.forward: action=%s"%(action.toString()))

        isTerminal = False
        scores     = []
        infos      = []
        pu         = self.public_state
        pr         = self.private_state

        if action.option == OptionSpace.Fold:
            self.action_fold(action)
        elif action.option == OptionSpace.Check:
            self.action_check(action)
        elif action.option == OptionSpace.Call:
            self.action_call(action)
        elif action.option == OptionSpace.Raise:
            self.action_raise(action)
        elif action.option == OptionSpace.AllIn:
            self.action_allin(action)
        else:
            raise Exception("action.option(%s) not in [Fold, Check, Call, Raise, AllIn]"%(action.option))

        # if it is time to computing_score
        if self.is_compute_score():
            isTerminal = True
            scores = self.compute_score()

        # if it is time to enter into the next stage
        if self.is_nextstage():
            add_cards = []
            if pu.stage == StageSpace.firstStage:   add_cards = pr.keep_cards[0:3]
            if pu.stage == StageSpace.secondStage:  add_cards = pr.keep_cards[3]
            if pu.stage == StageSpace.thirdStage:   add_cards = pr.keep_cards[4]

            pu.public_cards.append(add_cards)
            pu.stage = pu.stage + 1

        pu.previous_id                   = pu.turn
        pu.previous_action               = action
        pu.turn                          = self.next_player(pu.turn)

        infos = [Info() for i in xrange(self.public_state.num_players+1)]
        for i in xrange(len(infos)):
            infos[i].public_state = copy.deepcopy(self.public_state)
        infos[len(infos) - 1].private_state = copy.deepcopy(self.private_state)
        infos[pu.turn].available_actions = self.available_actions()

        if self.logger.level <= logging.DEBUG:
            self.logger.debug("TexasHoldemEnv.forward: num_quit+num_allin = %d+%d = %d"%(\
                self.public_state.num_quit,\
                self.public_state.num_allin,\
                self.public_state.num_quit + self.public_state.num_allin\
            ))

        return isTerminal, scores, infos

    #override
    @classmethod
    def round(cls, env, players):
        total_scores = [0    for i in xrange(len(players))]
        count        = 0

        ## the first match
        env.chips           = [5000 for i in xrange(len(players))]
        env.num_players     = len(players)
        env.dealer_id       = int(random.random * len(players))
        env.big_blind_bet   = 100

        isTerminal, _, infos = env.init()
        for i in xrange(len(players)):
            players[i].receive_info(infos[i])
        while isTerminal == False:
            turn = infos[-1].public_state.turn
            action = players[turn].take_action()
            isTerminal, scores, infos = env.forward(action)
            for i in xrange(len(players)):
                players[i].receive_info(infos[i])

        for i in xrange(len(players)):  total_scores[i] += scores[i]
        count += 1

        ## the following matches
        while True:
            dealer = (env.public_state.dealer_id + 1)%len(players)
            while env.public_state.chips[dealer]  == 0:
                dealer = (env.public_state.dealer_id + 1) % len(players)
            next_players_id = []  ## the available players (who still have bets) for the next match
            next_chips      = []
            next_dealer_id  = -1
            for i in xrange(len(env.public_state.chips)):
                if env.public_state.chips[i] > 0:
                    next_players_id.append(i)
                    next_chips.append(env.public_state.chips[i])
                    if i == dealer: next_dealer_id = len(next_players_id) - 1

            if len(next_players_id) == 1: break;

            if count % 10 == 0:
                env.big_blind_bet = env.big_blind_bet + 100
            env.chips       = next_chips
            env.dealer_id   = next_dealer_id
            env.num_players = len(next_players_id)
            isTerminal, _, infos = env.init()
            for i in xrange(len(next_players_id)):
                idx = next_players_id[i]
                players[idx].receive_info(infos[i])
            while isTerminal == False:
                turn = infos[-1].public_state.turn
                idx = next_players_id[turn]
                action = players[idx].take_action()
                isTerminal, scores, infos = env.forward(action)
                for i in xrange(len(next_players_id)):
                    idx = next_players_id[i]
                    players[idx].receive_info(infos[i])

            for i in xrange(len(next_players_id)):
                idx = next_players_id[i]
                total_scores[idx] += scores[i]
            count += 1

        for i in xrange(len(players)): total_scores[i] /= count * 1.0
        return total_scores;


    def next_player(self,i):
        pu = self.public_state

        p = (i+1)%pu.num_players
        while (pu.is_quit[p] or pu.is_allin[p]) and p != pu.flag_nextstage:
            p = (p+1)%pu.num_players

        return p


    def available_actions(self):
        '''
        :return: 
            A dict contains all available actions options
        '''
        return Utils.available_actions(self.public_state)


    def is_action_valid(self, action):
        '''
        :return: A boolean variable, which indicates whether is the action valid on the current state
        '''

        return Utils.is_action_valid(self.public_state, action)

    def is_nextstage(self):
        '''
        :return: 
        A boolean variable indicates whether is it time to enter the next stage
        '''
        pu = self.public_state
        return self.next_player(pu.turn) == pu.flag_nextstage

    def is_compute_score(self):
        '''
        :return: 
        A boolean variable indicates whether is it time to compute scores
        '''
        pu = self.public_state

        if pu.num_players ==  pu.num_quit + pu.num_allin:
            return True

        #need showdown
        if pu.stage == StageSpace.fourthStage and self.next_player(pu.turn) == pu.flag_nextstage:
            return True

        return False

    def compute_score(self):
        '''
        :return: a score array
        '''
        pu = self.public_state
        pr = self.private_state

        ## compute score before showdown, the winner takes all
        if pu.num_players  - 1 == pu.num_quit:
            scores = [0 for i in xrange(pu.num_players)]
            scores[pu.flag_nextstage] = sum(pu.bets)

        ## compute score after showdown
        else:
            scores                = [0 for i in xrange(pu.num_players)]
            playerid_pattern_bets = [] #for not_quit players
            for i in xrange(pu.num_players):
                if pu.is_quit[i] == True: continue
                hand_pattern = Utils.card2pattern(pr.hand_cards[i], pu.public_cards)
                playerid_pattern_bets.append((i,hand_pattern,pu.bets[i]))
            playerid_pattern_bets.sort(key=lambda x:x[1], cmp=Utils.compare_patterns)

            pot_line = 0
            previous = None
            tmp      = []
            for i in xrange(len(playerid_pattern_bets)-1,-1,-1):
                if previous == None:
                    tmp.append(playerid_pattern_bets[i])
                    previous = playerid_pattern_bets[i]
                elif Utils.compare_handcards(pu, pr.hand_cards,pr.hand_cards) == 0:
                    tmp.append(playerid_pattern_bets[i])
                    previous = playerid_pattern_bets[i]
                else:
                    tmp.sort(key = lambda x:x[2])
                    for i in xrange(len(tmp)):
                        num1 = len(tmp) - i
                        sum1 = 0
                        for p in xrange(pu.num_players):    sum1      += max(0, pu.bets[p] - pot_line)
                        for p in xrange(i, len(tmp)):       scores[p] += sum1 / num1
                        scores[pu.dealer_id] += sum1 % num1
                        if pot_line <= pu.bets[tmp[i][0]]: pot_line = pu.bets[tmp[i][0]]

                    previous = None
                    tmp      = []

            if len(tmp) > 0:
                tmp.sort(key = lambda  x:x[2])
                for i in xrange(len(tmp)):
                    num1 = len(tmp) - i
                    sum1 = 0
                    for p in xrange(pu.num_players):    sum1      += max(0, pu.bets[p] - pot_line)
                    for p in xrange(i, len(tmp)):       scores[p] += sum1 / num1
                    scores[pu.dealer_id] += sum1 % num1
                    if pot_line <= pu.bets[tmp[i][0]]: pot_line = pu.bets[tmp[i][0]]


        for p in xrange(pu.num_players):
            pu.chips[p] += scores[p]
            scores[p]   -= pu.bets[p]
        return scores


    def action_fold(self, action):
        pu = self.public_state
        pu.is_quit[pu.turn] = True
        pu.num_quit += 1

    def action_check(self, action):
        pass

    def action_call(self, action):
        pu = self.public_state
        pu.chips[pu.turn] -= action.price
        pu.bets[pu.turn]  += action.price


    def action_raise(self, action):
        pu = self.public_state
        pu.chips[pu.turn] -= action.price
        pu.bets[pu.turn]  += action.price
        pu.max_bet         = pu.bets[pu.turn]
        pu.flag_nextstage  = pu.turn

    def action_allin(self, action):
        pu = self.public_state

        pu.is_allin[pu.turn]   = True
        pu.num_allin          += 1

        pu.bets[pu.turn]      += action.price
        pu.max_bet             = action.price
        pu.flag_nextstage      = pu.turn
        pu.chips[pu.turn]      = 0
