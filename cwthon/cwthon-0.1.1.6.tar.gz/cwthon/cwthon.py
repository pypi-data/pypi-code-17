# -*- coding: utf-8 -*-
import logging
import requests
import cwthonUtil
import cwthonBase
from cwthonProp import *

contactDict = cwthonBase.updateContactDictCache()
roomDict = cwthonBase.updateRoomDictCache()

def getContactInfo(account_id : int) -> dict:
    contactInfo = contactDict.get(int(account_id))
    if contactInfo is None :
        contactDict.update(cwthonBase.updateContactDictCache())
        contactInfo = contactDict.get(int(account_id))
    return contactInfo

def getRoomInfo(room_id : int) -> dict:
    roomInfo = roomDict.get(int(room_id))
    if roomInfo is None :
        roomDict.update(cwthonBase.updateRoomDictCache())
        roomInfo = roomDict.get(int(room_id))
    return roomInfo

class cwReq(object):
    __endPoint = None
    __params = None
    def sendMsgToAccount(self, account_id : int, msg : str) -> cwRes:
        self.__endPoint = cwEndPoint.SEND_MSG
        self.__params = getContactInfo(account_id)
        self.__params.update({'body' : msg})
        return self.__send()

    def sendMsgToRoom(self, room_id : int, msg : str) -> cwRes:
        self.__endPoint = cwEndPoint.SEND_MSG
        self.__params = getRoomInfo(room_id)
        self.__params.update({'body' : msg})
        return self.__send()

    def __send(self) -> cwRes:
        method = self.__endPoint.value['method']
        if method is None :
            logging.error("cwReq cant send. method was None")
            return

        endPointUrl = self.__getEndPointUrl()

        res = None

        if method is reqMethods.POST:
            res = requests.post(
                url=endPointUrl,
                headers=cwthonBase.reqHdr,
                data={'body' : self.__params['body']}
                )
        elif method is reqMethods.GET:
            logging.error('send GET req Not implemented')
        elif method is reqMethods.DELETE:
            logging.error('send DELTE req is Not implemented')

        return cwRes(res)

    def __getEndPointUrl(self) -> str:
        path = cwthonUtil.replaceParam(
            target = self.__endPoint.value['url'],
            params = self.__params)
        return cwthonBase.baseUrl + path

class cwRes:
    def __init__(self, res):
        self.res = res