import requests,json,time,threading
class GilCalc:
    
    #quantapi.gilcalc.com 127.0.0.1
    def __init__(self,uid,usecret):
        self.__remoteip="quantapi.gilcalc.com"
        urltoken="http://{0}:10625/OAuth/Token".format(self.__remoteip)
        payload = "client_id={0}&client_secret={1}&grant_type=client_credentials"
        tokenheaders = {
    'content-type': "application/x-www-form-urlencoded",
    'cache-control': "no-cache",
    }
        response = requests.request("POST", urltoken, data=payload.format(uid,usecret), headers=tokenheaders)
        jsonTxt=json.loads(response.text)
        self.__token=jsonTxt['access_token']
        self.__refreshtoken=jsonTxt['refresh_token']
        self.__expires_in=jsonTxt['expires_in']
        self.__client_id=uid
        self.__client_secret=usecret
        #self.__LoadCode()
        print("登录成功..")
        #刷新token 提前1分钟刷新
        timer = threading.Timer(self.__expires_in-60, self.__RefreshToken)
        timer.start()
    def SingleCalc(self,funcname,*args):
        urlapi="http://{0}:38515/api/Calc/SingleCalc".format(self.__remoteip)
        arg=",".join([str(x) for x in args])
        querystring = {"Func":"{0}({1})".format(funcname,arg)}
        #print(in_json)
        headers = {
    'authorization': "Bearer  {0}".format(self.__token),
    'content-type': "application/json",
    'accept-charset': "utf-8",
    'cache-control': "no-cache",
    }
        response = requests.request("GET", urlapi,headers=headers,params=querystring)
        return json.loads(response.text)
   
    def BatchCalc(self,arrexp=[]):
        payload =arrexp
        in_json = json.dumps(payload)
        #print(in_json)
        headers = {
    'authorization': "Bearer  {0}".format(self.__token),
    'content-type': "application/json",
    'accept-charset': "utf-8",
    'cache-control': "no-cache",
    }
        url="http://{0}:38515/api/Calc/BatchCalc".format(self.__remoteip)
        response = requests.request("POST", url,data=in_json, headers=headers)
        return json.loads(response.text)

    def __RefreshToken(self):
        urltoken="http://{0}:10625/OAuth/Token".format(self.__remoteip)
        payload = "client_id={0}&client_secret={1}&grant_type=refresh_token&refresh_token={2}"
        tokenheaders = {
    'content-type': "application/x-www-form-urlencoded",
    'cache-control': "no-cache",
    }
        response = requests.request("POST", urltoken, data=payload.format(self.__client_id,self.__client_secret,self.__refreshtoken), headers=tokenheaders)
        jsonTxt=json.loads(response.text)
        self.__token=jsonTxt['access_token']
        self.__refreshtoken=jsonTxt['refresh_token']
        self.__expires_in=jsonTxt['expires_in']
        timer = threading.Timer(self.__expires_in-60, self.__RefreshToken)
        timer.start()
        
