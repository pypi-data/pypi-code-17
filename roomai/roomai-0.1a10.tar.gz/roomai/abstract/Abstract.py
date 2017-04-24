#!/bin/python
#coding=utf8

import copy

### abstract data struct
class AbstractPublicState:
    pass

class AbstractPrivateState:
    pass

class AbstractInfo:
    def __init__(self, public_state, private_state):

        ## public state information, which is available for all players
        self.public_state       = None

        ## private state information, which is unavailable for all players
        self.private_state      = None
        
        ## all available_actions for the current turn player
        self.available_actions  = None

    def get_public_state(self):
        return self.public_state

    def get_private_state(self):
        return self.private_state

    def get_available_actions(self):
        return self.available_actions


### abstract 
class AbstractPlayer:

    def receive_info(self, info):
        '''
        :param:
            info: the information produced by a game environments 
        :raises:
            NotImplementedError: An error occurred when we doesn't implement this function
        '''
        raise NotImplementedError("The receiveInfo function hasn't been implemented") 

    def take_action(self):
        '''
        :return: A Action produced by this player
        '''
        raise NotImplementedError("The takeAction function hasn't been implemented") 

    def reset(self):
        raise NotImplementedError("The reset function hasn't been implemented")


class AbstractEnv:

    def init(self):
        raise NotImplementedError("The init function hasn't been implemented")

    def forward(self, action):
        raise NotImplementedError("The receiveAction hasn't been implemented")

    @classmethod
    def round(cls, env, players):
        raise NotImplementedError("The round function hasn't been implemented")