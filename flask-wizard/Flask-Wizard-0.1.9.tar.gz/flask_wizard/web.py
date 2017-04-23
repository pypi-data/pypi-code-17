from __future__ import absolute_import
from __future__ import print_function

import json
import requests

from flask import request
from actions import *

from .nlu import NLUParser

class HttpHandler(object):
    """
        HttpHandler acts as the interface to provide the Http
        channel for your bot. 
        It accepts the incoming message as a post request and then sends the 
        response as a Http response
    """
    def __init__(self,model,config, actions):
        with open(actions,"r") as jsonFile:
            self.actions = json.load(jsonFile)
        if model == "":
            self.nlu = None
        else:
            print("jere")
            self.nlu = NLUParser(model,config)
            print("Server running")

    def response(self, *args, **kwargs):
        """
          Take the message, parse it and respond
        """
        payload = request.get_data()
        payload = payload.decode('utf-8')
        data = json.loads(payload)
        message = data["message"]
        if self.nlu:
            intent, entities = self.nlu.parse(message)
            if intent in self.actions:
                func = eval(self.actions[intent])
                session = {}
                session['user'] = request.remote_addr
                session['intent'] = intent
                session['entities'] = entities
                session['message'] = message
                session['channel'] = 'web' 
                response = func(session)
                return str(response)
            else:
                return "Sorry, I couldn't understand that"
        else:
            return str(message)