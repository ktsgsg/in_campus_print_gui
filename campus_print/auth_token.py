import requests
import time
import json
from . import general as g

class tokens:
    tokenId = ""
    successurl = ""
    cookies = []
    
    def __init__(self,userid,password):
        try:
            url = 'https://slbsso.meijo-u.ac.jp/opensso/json/authenticate'
            

            headers = {
                'Content-Type' : 'application/json'
            }
            source = requests.post(url,headers=headers)
            g.truetatuscode(source.status_code,200)
            #print("template loaded")
            jsn = json.loads(source.text)
            self.cookies = source.cookies.get_dict()
            jsn["callbacks"][0]["input"][0]["value"] = userid
            jsn["callbacks"][1]["input"][0]["value"] = password
            statuscode = 0
            for i in range(20):
                token = requests.post(url,headers=headers,json=jsn)
                statuscode = token.status_code
                #print(statuscode)
                if statuscode == 200:
                    break
                time.sleep(0.5)
                
            succesURL = json.loads(token.text)
            self.tokenId = succesURL["tokenId"]
            self.successurl = succesURL["successUrl"]
            
            
        except:
            #print("tokenidを取得できませんでした")
            raise BaseException("tokenを取得することができませんでした.時間をおいて再度試してください.")