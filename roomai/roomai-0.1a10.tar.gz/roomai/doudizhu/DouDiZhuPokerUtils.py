#!/bin/python
#coding:utf-8

import os
import roomai.abstract
import copy
import itertools


class Utils:
    gen_allactions = False

    @classmethod
    def is_action_valid(cls, hand_cards, public_state, action):
        if cls.gen_allactions == True:
            return True

        if action.pattern[0] == "i_invalid":
            return False

        if Utils.is_action_from_handcards(hand_cards, action) == False:
            return False

        turn = public_state.turn
        license_id = public_state.license_playerid
        license_act = public_state.license_action
        phase = public_state.phase

        if phase == PhaseSpace.bid:
            if action.pattern[0] not in ["i_cheat", "i_bid"]:
                return False
            return True

        if phase == PhaseSpace.play:
            if action.pattern[0] == "i_bid":    return False

            if public_state.is_response == False:
                if action.pattern[0] == "i_cheat": return False
                return True

            else:  # response
                if action.pattern[0] == "i_cheat":  return True
                ## not_cheat
                if action.pattern[6] > license_act.pattern[6]:
                    return True
                elif action.pattern[6] < license_act.pattern[6]:
                    return False
                elif action.maxMasterPoint - license_act.maxMasterPoint > 0:
                    return True
                else:
                    return False

    @classmethod
    def is_action_from_handcards(cls, hand_cards, action):
        flag = True
        if action.pattern[0] == "i_cheat":  return True
        if action.pattern[0] == "i_bid":    return True
        if action.pattern[0] == "i_invalid":    return False

        for a in action.masterPoints2Count:
            flag = flag and (action.masterPoints2Count[a] <= hand_cards.cards[a])
        for a in action.slavePoints2Count:
            flag = flag and (action.slavePoints2Count[a] <= hand_cards.cards[a])
        return flag

    @classmethod
    def action2pattern(cls, action):

        action.masterPoints2Count = dict()
        for c in action.masterCards:
            if c in action.masterPoints2Count:
                action.masterPoints2Count[c] += 1
            else:
                action.masterPoints2Count[c] = 1

        action.slavePoints2Count = dict()
        for c in action.slaveCards:
            if c in action.slavePoints2Count:
                action.slavePoints2Count[c] += 1
            else:
                action.slavePoints2Count[c] = 1

        action.isMasterStraight = 0
        num = 0
        for v in action.masterPoints2Count:
            if (v + 1) in action.masterPoints2Count and (v + 1) < ActionSpace.two:
                num += 1
        if num == len(action.masterPoints2Count) - 1 and len(action.masterPoints2Count) != 1:
            action.isMasterStraight = 1

        action.maxMasterPoint = -1
        action.minMasterPoint = 100
        for c in action.masterPoints2Count:
            if action.maxMasterPoint < c:
                action.maxMasterPoint = c
            if action.minMasterPoint > c:
                action.minMasterPoint = c

        ########################
        ## action 2 pattern ####
        ########################


        # is cheat?
        if len(action.masterCards) == 1 \
                and len(action.slaveCards) == 0 \
                and action.masterCards[0] == ActionSpace.cheat:
            action.pattern = AllPatterns["i_cheat"]

        # is roblord
        elif len(action.masterCards) == 1 \
                and len(action.slaveCards) == 0 \
                and action.masterCards[0] == ActionSpace.bid:
            action.pattern = AllPatterns["i_bid"]

        # is twoKings
        elif len(action.masterCards) == 2 \
                and len(action.masterPoints2Count) == 2 \
                and len(action.slaveCards) == 0 \
                and action.masterCards[0] in [ActionSpace.r, ActionSpace.R] \
                and action.masterCards[1] in [ActionSpace.r, ActionSpace.R]:
            action.pattern = AllPatterns["x_rocket"]

        else:

            ## process masterCards
            masterPoints = action.masterPoints2Count
            if len(masterPoints) > 0:
                count = masterPoints[action.masterCards[0]]
                for c in masterPoints:
                    if masterPoints[c] != count:
                        action.pattern = AllPatterns["i_invalid"]

            if action.pattern == None:
                pattern = "p_%d_%d_%d_%d_%d" % (len(action.masterCards), len(masterPoints), \
                                                action.isMasterStraight, \
                                                len(action.slaveCards), 0)

                if pattern in AllPatterns:
                    action.pattern = AllPatterns[pattern]
                else:
                    action.pattern = AllPatterns["i_invalid"]

        return action

    @classmethod
    def extractMasterCards(cls, hand_cards, numPoint, count, pattern):
        is_straight = pattern[3]
        cardss = []
        ss = []

        if numPoint == 0:
            return cardss

        if is_straight == 1:
            c = 0
            for i in xrange(11, -1, -1):
                if hand_cards.cards[i] >= count:
                    c += 1
                else:
                    c = 0

                if c >= numPoint:
                    ss.append(range(i, i + numPoint))
        else:
            candidates = []
            for c in xrange(len(hand_cards.cards)):
                if hand_cards.cards[c] >= count:
                    candidates.append(c)
            if len(candidates) < numPoint:
                return []
            ss = list(itertools.combinations(candidates, numPoint))

        for set1 in ss:
            s = []
            for c in set1:
                for i in xrange(count):
                    s.append(c)
            s.sort()
            cardss.append(s)

        return cardss

    @classmethod
    def extractSlaveCards(cls, hand_cards, numCards, used_cards, pattern):
        used = [0 for i in xrange(15)]
        for p in used_cards:
            used[p] += 1

        numMaster = pattern[1]
        numMasterPoint = pattern[2]
        numSlave = pattern[4]

        candidates = []
        res1 = []
        res = []

        if numMaster / numMasterPoint == 3:
            if numSlave / numMasterPoint == 1:  # single
                for c in xrange(len(hand_cards.cards)):
                    if used[c] == 0 and ((hand_cards.cards[c] - used[c])) >= 1:
                        candidates.append(c)
                if len(candidates) >= numCards:
                    res1 = list(set(list(itertools.combinations(candidates, numCards))))
                for sCard in res1:  res.append([x for x in sCard])

            elif numSlave / numMasterPoint == 2:  # pair
                for c in xrange(len(hand_cards.cards)):
                    if (hand_cards.cards[c] - used[c]) >= 2 and used[c] == 0:
                        candidates.append(c)
                if len(candidates) >= numCards / 2:
                    res1 = list(set(list(itertools.combinations(candidates, numCards / 2))))
                for sCard in res1:
                    tmp = [x for x in sCard]
                    tmp.extend([x for x in sCard])
                    res.append(tmp)

        elif numMaster / numMasterPoint == 4:

            if numSlave / numMasterPoint == 2:  # single
                for c in xrange(len(hand_cards.cards)):
                    if used[c] == 0 and (hand_cards.cards[c] - used[c]) >= 1:
                        candidates.append(c)
                if len(candidates) >= numCards:
                    res1 = list(set(list(itertools.combinations(candidates, numCards))))
                for sCard in res1:  res.append([x for x in sCard])


            elif numSlave / numMasterPoint == 4:  # pair
                for c in xrange(len(hand_cards.cards)):
                    if (hand_cards.cards[c] - used[c]) >= 2 and used[c] == 0:
                        candidates.append(c)
                if len(candidates) >= numCards / 2:
                    res1 = list(set(list(itertools.combinations(candidates, numCards / 2))))
                for sCard in res1:
                    tmp = [x for x in sCard]
                    tmp.extend([x for x in sCard])
                    res.append(tmp)

        return res

    @classmethod
    def lookup_action(cls, masterCards, slaveCards):
        masterCards.sort()
        slaveCards.sort()

        key_int = (masterCards + slaveCards)
        key_str = []
        for i in key_int:
            key_str.append(ActionSpace.key_to_str[i])
        key_str.sort()
        key = "".join(key_str)

        if cls.gen_allactions == True:
            return key, Action(masterCards, slaveCards)

        if key in AllActions:
            return key, AllActions[key]
        else:
            raise Exception(key + "is not in AllActions")

    @classmethod
    def lookup_action_by_key(cls, key):
        if key in AllActions:
            return key, AllActions[key]
        else:
            raise Exception(key + "is not in AllActions")

    @classmethod
    def candidate_actions(cls, hand_cards, public_state):

        patterns = []
        if public_state.phase == PhaseSpace.bid:
            patterns.append(AllPatterns["i_cheat"])
            patterns.append(AllPatterns["i_bid"])
        else:
            if public_state.is_response == False:
                for p in AllPatterns:
                    if p != "i_cheat" and p != "i_invalid":
                        patterns.append(AllPatterns[p])
            else:
                patterns.append(public_state.license_action.pattern)
                if public_state.license_action.pattern[6] == 1:
                    patterns.append(AllPatterns["p_4_1_0_0_0"])  # rank = 10
                    patterns.append(AllPatterns["x_rocket"])  # rank = 100
                if public_state.license_action.pattern[6] == 10:
                    patterns.append(AllPatterns["x_rocket"])  # rank = 100
                patterns.append(AllPatterns["i_cheat"])

        is_response = public_state.is_response
        license_act = public_state.license_action
        actions = dict()

        for pattern in patterns:
            numMaster = pattern[1]
            numMasterPoint = pattern[2]
            isStraight = pattern[3]
            numSlave = pattern[4]
            MasterCount = -1
            SlaveCount = -1

            if numMaster > 0:
                MasterCount = numMaster / numMasterPoint

            if "i_invalid" == pattern[0]:
                continue

            if "i_cheat" == pattern[0]:
                key, action = cls.lookup_action([ActionSpace.cheat], [])
                if cls.is_action_valid(hand_cards, public_state, action) == True:
                    actions[key] = action
                continue

            if "i_bid" == pattern[0]:
                key, action = cls.lookup_action([ActionSpace.bid], [])
                if cls.is_action_valid(hand_cards, public_state, action) == True:
                    actions[key] = action
                continue

            if pattern[0] == "x_rocket":
                if hand_cards.cards[ActionSpace.r] == 1 and \
                                hand_cards.cards[ActionSpace.R] == 1:
                    key, action = cls.lookup_action([ActionSpace.r, ActionSpace.R], [])
                    if cls.is_action_valid(hand_cards, public_state, action) == True:
                        actions[key] = action
                continue

            if pattern[1] + pattern[4] > hand_cards.num_cards:
                continue
            sum1 = 0
            for count in xrange(MasterCount, 5, 1):
                sum1 += hand_cards.count2num[count]
            if sum1 < numMasterPoint:
                continue

            ### action with cards
            mCardss = []
            mCardss = Utils.extractMasterCards(hand_cards, numMasterPoint, MasterCount, pattern)

            for mCards in mCardss:
                if numSlave == 0:
                    key, action = cls.lookup_action(mCards, [])
                    if cls.is_action_valid(hand_cards, public_state, action) == True:
                        actions[key] = action
                    continue

                sCardss = Utils.extractSlaveCards(hand_cards, numSlave, mCards, pattern)
                for sCards in sCardss:
                    key, action = cls.lookup_action(mCards, sCards)
                    if cls.is_action_valid(hand_cards, public_state, action) == True:
                        actions[key] = action
        return actions

#
#0, 1, 2, 3, ..., 7,  8, 9, 10, 11, 12, 13, 14
#^                ^   ^              ^       ^
#|                |   |              |       |
#3,               10, J, Q,  K,  A,  2,  r,  R
#

class PhaseSpace:
    bid  = 0
    play = 1


class ActionSpace:
    str_to_key  = {'3':0, '4':1, '5':2, '6':3, '7':4, '8':5, '9':6, 'T':7, 'J':8, 'Q':9, 'K':10, 'A':11, '2':12, 'r':13, 'R':14, 'x':15, 'b':16}
    # x means check, b means bid
    key_to_str  = {0: '3', 1:'4', 2:'5', 3:'6', 4:'7', 5:'8', 6:'9', 7:'T', 8:'J', 9:'Q', 10:'K', 11:'A', 12:'2', 13:'r', 14:'R', 15:'x', 16:'b'}
    three       = 0;
    four        = 1;
    five        = 2;
    six         = 3;
    seven       = 4;
    eight       = 5;
    night       = 6;
    ten         = 7;
    J           = 8;
    Q           = 9;
    K           = 10;
    A           = 11;
    two         = 12;
    r           = 13;
    R           = 14;
    cheat       = 15;
    bid         = 16;

    total_normal_cards = 15

class HandCards:
    def __init__(self, cardstr):
        self.cards      = [0 for i in xrange(ActionSpace.total_normal_cards)]
        for c in cardstr:
            idx = ActionSpace.str_to_key[c]
            self.cards[idx] += 1
            if idx >= ActionSpace.total_normal_cards:
                raise Exception("%s is invalid for a handcard"%(cardstr))
        
        self.num_cards    = sum(self.cards)
        self.count2num    = [0 for i in xrange(ActionSpace.total_normal_cards)]
        for count in self.cards:
            self.count2num[count] += 1

        strs = []
        for h in xrange(len(self.cards)):
            for count in xrange(self.cards[h]):
                strs.append(ActionSpace.key_to_str[h])
        strs.sort()
        self.String = "".join(strs)


    def toString(self, is_recomputing=False):
        if is_recomputing == False:
            return self.String
        else:
            strs = []
            for h in xrange(len(self.cards)):
                for count in xrange(self.cards[h]):
                    strs.append(ActionSpace.key_to_str[h])
            strs.sort()
            return "".join(strs)

    def add_cards_str(self, str):
        self.add_cards(HandCards(str))
        self.String = self.toString(is_recomputing=True)


    def add_cards(self, cards):
        for c in xrange(len(cards.cards)):
            count                         = cards.cards[c]
            self.num_cards                += count
            self.count2num[self.cards[c]] -= 1
            self.cards[c]                 += count
            self.count2num[self.cards[c]] += 1

        self.String = self.toString(is_recomputing=True)

    def remove_cards_str(self, str):
        self.remove_cards(HandCards(str))
        self.String = self.toString(is_recomputing=True)

    def remove_cards(self, cards):
        for c in xrange(len(cards.cards)):
            count = cards.cards[c]
            self.num_cards                -=count
            self.count2num[self.cards[c]] -= 1
            self.cards[c]                 -=count
            self.count2num[self.cards[c]] += 1

        self.String = self.toString(is_recomputing=True)

    def remove_action(self, action):
        str = action.toString()
        if str == 'x' or str == 'b':
            str = ''
        self.remove_cards(HandCards(str))
        self.String = self.toString(is_recomputing=True)


class Action:
    def __init__(self, masterCards, slaveCards):
        self.masterCards        = copy.deepcopy(masterCards)
        self.slaveCards         = copy.deepcopy(slaveCards)

        self.masterPoints2Count = None
        self.slavePoints2Count  = None
        self.isMasterStraight   = None
        self.maxMasterPoint     = None
        self.minMasterPoint     = None
        self.pattern            = None
        Utils.action2pattern(self)

        key_int = (self.masterCards + self.slaveCards)
        key_str = []
        for key in key_int:
            key_str.append(ActionSpace.key_to_str[key])
        key_str.sort()
        self.String = "".join(key_str)


    def toString(self):
        return self.String



############## read data ################
AllPatterns = dict()
AllActions = dict()
import zipfile
def get_file(path):
    if ".zip" in path:
        lines = path.split(".zip")
        zip1 = zipfile.ZipFile(lines[0] + ".zip")
        len1 = len(lines[1])
        path = lines[1][1:len1]
        return zip1.open(path)
    else:
        return open(path)
path = os.path.split(os.path.realpath(__file__))[0]
pattern_file = get_file(path + "/patterns.py")
for line in pattern_file:
    line = line.replace(" ", "").strip()
    line = line.split("#")[0]
    if len(line) == 0:  continue
    lines = line.split(",")
    for i in xrange(1, len(lines)):
        lines[i] = int(lines[i])
    AllPatterns[lines[0]] = lines
pattern_file.close()

action_file = get_file(path + "/actions.py")
for line in action_file:
    line = line.replace(" ", "").strip()
    lines = line.split("\t")

    m = []
    ms = lines[0].split(",")
    for c in ms:
        if c != "":
            m.append(int(c))

    s = []
    ss = []
    if len(lines) == 2:
        ss = lines[1].split(",")
    for c in ss:
        if c != "":
            s.append(int(c))
    action = Action(m, s)
    AllActions[action.toString()] = action
action_file.close()


class PrivateState(roomai.abstract.AbstractPrivateState):
    def __init__(self):
        self.hand_cards     = [[],[],[]]
        self.keep_cards     = []

class PublicState(roomai.abstract.AbstractPublicState):
    def __init__(self):
        self.landlord_candidate_id  = -1
        self.landlord_id            = -1
        self.license_playerid       = -1
        self.license_action         = None
        self.is_response            = False

        self.first_player           = -1
        self.turn                   = -1
        self.phase                  = -1
        self.epoch                  = -1

        self.previous_id            = -1
        self.previous_action        = None


class Info(roomai.abstract.AbstractInfo):
    def __init__(self):
        ### init
        self.init_id            = None
        self.init_cards         = None
        self.init_addcards      = None

        self.public_state       = None
        #In the info sent to players, the private info always be None.
        self.private_state      = None
        self.available_actions  = None

