# Setup
import requests

statusendpoint = 'http://status.memework.org/api'

def core():
    """memestatus.core()

    Initalizes memestatus (already done by the other files)"""
    apiget = requests.get(statusendpoint)
    apires = apiget.json()
