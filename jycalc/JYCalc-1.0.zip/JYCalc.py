import requests,json,threading
class JYCalc:
    def __init__(self,uid,usecret):
        self.urltoken="http://10.1.43.56:11625/OAuth/Token"
        payload = "client_id={0}&client_secret={1}&grant_type=client_credentials"
        self.tokenheaders = {
    'content-type': "application/x-www-form-urlencoded",
    'cache-control': "no-cache",
    }
        response = requests.request("POST", self.urltoken, data=payload.format(uid,usecret), headers=self.tokenheaders)
        jsonTxt=json.loads(response.text)
        self.token=jsonTxt['access_token']
        self.refreshtoken=jsonTxt['refresh_token']
        self.expires_in=jsonTxt['expires_in']
        self.client_id=uid
        self.client_secret=usecret
        self.urlapi="http://10.1.43.56:38385/api/Calc/SingleCalc"
        self.__LoadCode()
        print("登录成功..")
        #刷新token 提前1分钟刷新
        timer = threading.Timer(self.expires_in-60, self.__RefreshToken)
        timer.start()
    def iCalc(self,funcname,*expression):
        payload ={"IndicatorName":funcname,"ListParams":expression}
        in_json = json.dumps(payload)
        #print(in_json)
        headers = {
    'authorization': "Bearer  {0}".format(self.token),
    'content-type': "application/json",
    'accept-charset': "utf-8",
    'cache-control': "no-cache",
    }
        response = requests.request("POST", self.urlapi,data=in_json, headers=headers)
        return response.text
    def __LoadCode(self):
       t=self.iCalc("GC_SECUMAINFORM_Query",8)
       r=json.loads(t)
       self.SecuCodeCache=r["Result"]
       
    def GetInnerCode(self,secucode,*market):
        for secuInfo in self.SecuCodeCache:
            if(len(market)==0):
                if(str(secuInfo["SecuCode"])+str(secuInfo["Suffix"]) == secucode or str(secuInfo["SecuCode"]) == secucode):
                    return secuInfo["InnerCode"]
    def __RefreshToken(self):
        payload = "client_id={0}&client_secret={1}&grant_type=refresh_token&refresh_token={2}"
        response = requests.request("POST", self.urltoken, data=payload.format(self.client_id,self.client_secret,self.refreshtoken), headers=self.tokenheaders)
        jsonTxt=json.loads(response.text)
        self.token=jsonTxt['access_token']
        self.refreshtoken=jsonTxt['refresh_token']
        self.expires_in=jsonTxt['expires_in']
        timer = threading.Timer(self.expires_in-60, self.__RefreshToken)
        timer.start()
        return 0
        

           
                
                
                
         
        
        
        

        
    
      
            
            


        
