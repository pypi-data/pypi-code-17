# Made by Vilhelm Prytz 2017
# Copyright 2017

def getIP_all():
    from sys import version_info
    py3 = version_info[0] > 2
    if py3:
        import urllib.request
        req = urllib.request.Request("https://ip-api.mrkakisen.net/api/v1/plainText/")
        ipFetch = urllib.request.urlopen(req)
        if ipFetch == None or ipFetch.getcode() != 200:
            print("Error! No connection to internet.")
            quit(0)
        else:
            return(str(ipFetch.read()))
    else:
        import urllib
        ipFetch = urllib.urlopen("https://ip-api.mrkakisen.net/api/v1/plainText/")
        if ipFetch == None or ipFetch.getcode() != 200:
            print("Error! No connection to internet.")
            quit(0)
        else:
            return(str(ipFetch.read()))
