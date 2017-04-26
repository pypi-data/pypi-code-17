import json
import requests
import chatwork
import _base

if __name__ == '__main__':
    res = requests.get(
        url='https://api.chatwork.com/v2/me',
        headers=_base.reqHdr)
    print(res.text)
    myData = json.loads(res.text)

    msgAc = 'test from account_id'
    account_id = myData['account_id']
    msgRo = 'test from room_id'
    room_id = myData['room_id']

    print("account_id[" + str(account_id) + "]")
    print("room_id[" + str(room_id) + "]")

    cwReq = chatwork.cwReq()
    #cwReq.sendMsgToAccount(account_id=account_id, msg=msgAc)
    cwReq.sendMsgToRoom(room_id=room_id, msg=msgRo)
