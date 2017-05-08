#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Login SCRAM operations.... from Javascript...
"""
import random

def create_client_first_message():
    """
            function() {
            var b = c._random(4);
            this._clientNonce = a.codec.base64.fromBits(b);
            this._clientFirstMessageBare = c._createClientFirstMessageBare(this._username, this._clientNonce);
            return "n,," + this._clientFirstMessageBare
        };
    """
    
    pass


def _random():
    """
        a = 4
        c._random = function(a) {
        for (var c = [], b = 0; b < a; b++) c.push(4294967296 * Math.random() | 0);
        return c
    """
    c = []
    for x in range (0,4):
        c.append(int(4294967296 * random.random()) | 0)