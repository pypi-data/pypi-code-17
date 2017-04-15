import os
import sys
import json

def getconfigfile():
    try:
        return json.load(open("./nephelo.json", "r"))
    except Exception as e:
        print "There was an error loading the config file. Expected at ./nephelo.json"
        print e
    return None

