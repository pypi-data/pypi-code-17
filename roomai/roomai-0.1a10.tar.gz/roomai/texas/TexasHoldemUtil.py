#!/bin/python
#coding:utf-8

import roomai.abstract

class StageSpace:
    firstStage  = 1
    secondStage = 2
    thirdStage  = 3
    fourthStage = 4

class OptionSpace:
    # 弃牌
    Fold        = "fold"
    # 过牌
    Check       = "check"
    # 更注
    Call        = "call"
    # 加注
    Raise       = "raise"
    # all in
    AllIn       = "allin"

point_str_to_key  = {'2':0,'3':1, '4':2, '5':3, '6':4, '7':5, '8':6, '9':7, 'T':8, 'J':9,  'Q':10, 'K':11,  'A':12}
point_key_to_str  = {0:'2', 1:'3', 2:'4', 3:'5', 4:'6', 5:'7', 6:'8', 7:'9', 8:'T', 9:'J', 10:'Q',  11:'K',  12:'A'}
suit_key_to_str   = {0:'Spade',    1:'Heart',       2:'Diamond',       3:'Club'}
suit_str_to_key   = {'Spade':0,    'Heart':1,       'Diamond':2,       'Club':3}
class Card:
    def __init__(self, point, suit):
        point1 = point
        if isinstance(point, str):
            point1 = point_str_to_key[point]
        suit1  = suit
        if isinstance(suit, str):
            suit1 = suit_str_to_key[suit]

        self.point  = point1
        self.suit   = suit1
        self.String = "%s_%s"%(point_key_to_str[point1], suit_key_to_str[suit1])

    def toString(self):
        return self.String


AllCardsPattern = dict() 
#0     1           2       3           4                                    5     6     
#name, isStraight, isPair, isSameSuit, [SizeOfPair1, SizeOfPair2,..](desc), rank, cards
AllCardsPattern["Straight_SameSuit"] = \
["Straight_SameSuit",   True,  False, True,  [],        100, []]
AllCardsPattern["4_1"] = \
["4_1",                 False, True,  False, [4,1],     98,  []]
AllCardsPattern["3_2"] = \
["3_2",                 False, True,  False, [3,2],     97,  []]
AllCardsPattern["SameSuit"] = \
["SameSuit",            False, False, True,  [],        96,  []]
AllCardsPattern["Straight_DiffSuit"] = \
["Straight_DiffSuit",   True,  False, False, [],        95,  []]
AllCardsPattern["3_1_1"] = \
["3_1_1",               False, True,  False, [3,1,1],   94,  []]
AllCardsPattern["2_2_1"] = \
["2_2_1",               False, True,  False, [2,2,1],   93,  []]
AllCardsPattern["2_1_1_1"] = \
["2_1_1_1",             False, True,  False, [2,1,1,1], 92,  []]


class Action:
    def __init__(self, option1, price):
        self.option = option1
        self.price  = price
        self.String = "%s_%d"%(self.option, self.price)
    def toString(self):
        return self.String

class PublicState(roomai.abstract.AbstractPublicState):
    def __init__(self):
        self.stage              = None
        self.num_players        = None
        self.dealer_id          = None
        self.public_cards       = None
        self.is_quit            = None
        self.num_quit           = None
        self.is_allin           = None
        self.num_allin          = None
        self.num_players        = None
        self.big_blind_bet      = None

        # who is expected to take a action
        self.turn               = None

        #chips is array which contains the chips of all players
        self.chips              = None

        #bets is array which contains the bets from all players
        self.bets               = None

        #max_bet = max(self.bets)
        self.max_bet            = None
        #the raise acount
        self.raise_account      = None

        # it is time to enter into the next stage or showdown,
        # when next_player == flag_for_nextstage
        self.flag_nextstage = None

        self.previous_id        = None
        self.previous_action    = None        

class PrivateState(roomai.abstract.AbstractPrivateState):
    def __init__(self):
        self.keep_cards = None
        self.hand_cards = None

class Info(roomai.abstract.AbstractInfo):
    def __init__(self):
        self.init_player_id          = None
        self.init_hand_cards         = None
        #player_id and hand_cards will be sent to players at the begining of game

        self.public_state            = None
        self.private_state           = None
        self.available_actions       = None

class Utils:
    @classmethod
    def compare_cards(cls, c1, c2):
            if c1.point != c2.point:
                return c1.point - c2.point
            else:
                return c1.suit - c2.suit

    @classmethod
    def cards2pattern(cls, hand_cards, remaining_cards):
        point2cards = dict()
        for c in hand_cards + remaining_cards:
            if c.point in point2cards:
                point2cards[c.point].append(c)
            else:
                point2cards[c.point] = [c]
        for p in point2cards:
            point2cards[p].sort(Utils.compare_cards)

        suit2cards = dict()
        for c in hand_cards + remaining_cards:
            if c.suit in suit2cards:
                suit2cards[c.suit].append(c)
            else:
                suit2cards[c.suit] = [c]
        for s in suit2cards:
            suit2cards[s].sort(Utils.compare_cards)

        num2point = [[], [], [], [], []]
        for p in point2cards:
            num = len(point2cards[p])
            num2point[num].append(p)
        for i in xrange(5):
            num2point[num].sort()

        sorted_point = []
        for p in point2cards:
            sorted_point.append(p)
        sorted_point.sort()

        ##straight_samesuit
        for s in suit2cards:
            if len(suit2cards[s]) >= 5:
                numStraight = 1
                for i in xrange(len(suit2cards[s]) - 2, -1, -1):
                    if suit2cards[s][i].point == suit2cards[s][i + 1].point - 1:
                        numStraight += 1
                    else:
                        numStraight = 1

                    if numStraight == 5:
                        pattern = AllCardsPattern["Straight_SameSuit"]
                        pattern[6] = suit2cards[s][i:i + 5]
                        return pattern

        ##4_1
        if len(num2point[4]) > 0:
            p4 = num2point[4][0]
            p1 = -1
            for i in xrange(len(sorted_point) - 1, -1, -1):
                if sorted_point[i] != p4:
                    p1 = sorted_point[i]
                    break
            pattern = AllCardsPattern["4_1"]
            pattern[6] = point2cards[p4][0:4]
            pattern[6].append(point2cards[p1][0])
            return pattern

        ##3_2
        if len(num2point[3]) >= 1:
            pattern = AllCardsPattern["3_2"]

            if len(num2point[3]) == 2:
                p3 = num2point[3][1]
                pattern[6] = point2cards[p3][0:3]
                p2 = num2point[3][0]
                pattern[6].append(point2cards[p2][0])
                pattern[6].append(point2cards[p2][1])
                return pattern

            if len(num2point[2]) >= 1:
                p3 = num2point[3][0]
                pattern[6] = point2cards[p3][0:3]
                p2 = num2point[2][len(num2point[2]) - 1]
                pattern[6].append(point2cards[p2][0])
                pattern[6].append(point2cards[p2][1])
                return pattern

        ##SameSuit
        for s in suit2cards:
            if len(suit2cards[s]) >= 5:
                pattern = AllCardsPattern["SameSuit"]
                len1 = len(suit2cards[s])
                pattern[6] = suit2cards[s][len1 - 5:len1]
                return pattern

        ##Straight_DiffSuit
        numStraight = 1
        for idx in xrange(len(sorted_point) - 2, -1, -1):
            if sorted_point[idx] + 1 == sorted_point[idx]:
                numStraight += 1
            else:
                numStraight = 1

            if numStraight == 5:
                pattern = AllCardsPattern["Straight_DiffSuit"]
                for p in xrange(idx, idx + 5):
                    point = sorted_point[p]
                    pattern[6].append(point2cards[point][0])
                return pattern

        ##3_1_1
        if len(num2point[3]) == 1:
            pattern = AllCardsPattern["3_1_1"]

            p3 = num2point[3][0]
            pattern[6] = point2cards[p3][0:3]

            num = 0
            for i in xrange(len(sorted_point) - 1, -1, -1):
                p = sorted_point[i]
                if p != p3:
                    pattern[6].append(point2cards[p][0])
                    num += 1
                if num == 2:    break
            return pattern

        ##2_2_1
        if len(num2point[2]) >= 2:
            pattern = AllCardsPattern["2_2_1"]
            p21 = num2point[2][len(num2point[2]) - 1]
            for c in point2cards[p21]:
                pattern[6].append(c)
            p22 = num2point[2][len(num2point[2]) - 2]
            for c in point2cards[p22]:
                pattern[6].append(c)

            flag = False
            for i in xrange(len(sorted_point) - 1, -1, -1):
                p = sorted_point[i]
                if p != p21 and p != p22:
                    c = point2cards[p][0]
                    pattern[6].append(c)
                    flag = True
                if flag == True:    break;
            return pattern

        ##2_1_1_1
        if len(num2point[2]) == 1:
            pattern = AllCardsPattern["2_1_1_1"]
            p2 = num2point[2][0]
            pattern[6] = point2cards[p2][0:2]
            num = 0
            for p in xrange(len(sorted_point) - 1, -1, -1):
                p1 = sorted_point[p]
                if p1 != p2:
                    pattern[6].append(point2cards[p1][0])
                if num == 3:    break
            return pattern

    @classmethod
    def compare_handcards(cls,hand_card0, hand_card1, keep_cards):
        pattern0 = Utils.cards2pattern(hand_card0, keep_cards)
        pattern1 = Utils.cards2pattern(hand_card1, keep_cards)
        
        diff = cls.compare_patterns(pattern0, pattern1)
        return diff

    @classmethod
    def compare_patterns(cls, p1, p2):
            if p1[5] != p2[5]:
                return p1[5] - p2[5]
            else:
                for i in xrange(5):
                    if p1[6][i] != p2[6][i]:
                        return p1[6][i] - p2[6][i]
                return 0

    @classmethod
    def available_actions(cls, public_state):
        pu = public_state
        turn = pu.turn
        key_actions = dict()

        ## for fold
        action = Action(OptionSpace.Fold,0)
        if cls.is_action_valid(public_state, action):
            key_actions[action.toString()] = action

        ## for check
        if pu.bets[turn] == pu.max_bet:
            action = Action(OptionSpace.Check, 0)
            if cls.is_action_valid(public_state, action):
                key_actions[action.toString()] = action

        ## for call
        if pu.bets[turn] != pu.max_bet and pu.chips[turn] > pu.max_bet - pu.bets[turn]:
            action = Action(OptionSpace.Call, pu.max_bet - pu.bets[turn])
            if cls.is_action_valid(public_state, action):
                key_actions[action.toString()] = action

        ## for raise
        if pu.bets[turn] != pu.max_bet and pu.chips[turn] > pu.max_bet - pu.bets[turn] + pu.raise_account:
            num = (pu.chips[turn] - (pu.max_bet - pu.bets[turn])) / pu.raise_account
            for i in xrange(1,num+1):
                action = Action(OptionSpace.Raise, (pu.max_bet - pu.bets[turn]) + pu.raise_account * i)
                if cls.is_action_valid(public_state, action):
                    key_actions[action.toString()] = action

        ## for all in
        action = Action(OptionSpace.AllIn, pu.chips[turn])
        if cls.is_action_valid(public_state, action):
           key_actions[action.toString()] = action

        return key_actions

    @classmethod
    def is_action_valid(cls, public_state, action):
        ps = public_state

        if (not isinstance(public_state,PublicState)) or (not isinstance(action, Action)):
            return False

        if ps.is_allin[ps.turn] == True or ps.is_quit[ps.turn] == True:
            return False
        if ps.chips[ps.turn] == 0:
            return False

        if action.option == OptionSpace.Fold:
            return True

        elif action.option == OptionSpace.Check:
            if ps.bets[ps.turn] == ps.max_bets:
                return True
            else:
                return False

        elif action.option == OptionSpace.Call:
            if action.price == ps.max_bet - ps.bets[ps.turn]:
                return True
            else:
                return False

        elif action.option == OptionSpace.Raise:
            raise_account = action.price - (ps.max_bet - ps.bets[ps.turn])
            if raise_account == 0:    return False
            if raise_account % ps.raise_account == 0:   return True
            else:   return False


        elif action.option == OptionSpace.AllIn:
            return True
        else:
            raise Exception("Invalid action.option"+action.option)


