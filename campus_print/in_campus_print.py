import requests
import json
from selenium import webdriver
import time
from .import auth_token as ath
from . import settings as s
from requests_toolbelt import MultipartEncoder

class Webprint:#printformatの設定に従って，printdataを印刷する
    
    url = f"https://ccmoon2.meijo-u.ac.jp/f5-w-68747470733a2f2f63636470737276312e6d65696a6f2d752e61632e6a70$$/user/f5-h-$$/api/spool01/files/webprint"
    filename = "abc.pdf"
    cookies = {}
    printformat = {}
    _defaultformat = {#privatedですよ
            "user_id":"0000",
            "queue_id":"web-ondemand",
            "ip":"0.0.0.0",
            "paper_type":"06",
            "duplex_type":"1",
            "color_mode_type":"1",
            "copies":"1",
            "number_up":"1",
            "orientation_edge":"1",
            "print_orientation":"2",
            "page_sort":"1"
        }
    def __init__(self,userdata):
        self.userdata = userdata
        self.cookies = self.get_cookies(userdata)
        self._defaultformat["ip"] = self._get_ownipaddress()
        self._defaultformat["user_id"] = userdata["userid"]
    def _get_ownipaddress(self):
        source = requests.get("https://ccmoon2.meijo-u.ac.jp/f5-w-68747470733a2f2f63636470737276312e6d65696a6f2d752e61632e6a70$$/user/f5-h-$$/user/f5-h-$$/api/system/notice/ownipaddress",
                                cookies=self.cookies)
        if source.status_code != 200:
            #print("ownip取得失敗.")
            return {}
        jsn = json.loads(source.text)
        return jsn["ip_address"]
    def pdfprint(self):#プリントの実行
        #print("プリントの実行")
        json_bytes = json.dumps(self.printformat).encode("utf-8")
        self.m = MultipartEncoder(
            fields={
                "data" : ("blob",json_bytes,"application/json"),
                "files" : (self.filename,open(self.printdatapath,"rb"),"application/pdf")
            },
            boundary="------geckoformboundary62e25ce6ff5a54f51fd44a79a4e0408c"
        )
        headers = {
        "Content-Type": self.m.content_type
        }
        source = requests.post(self.url,headers=headers,data=self.m,cookies=self.cookies)
        return source.status_code
    def get_cookies(self,userdata):#プリントに必要なcookieの取得
        tokens = ath.tokens(userdata["userid"],userdata["password"])#トークンの取得 modeはccmoon2
        #一回seleniumで試してみる．
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")#headlessmodeで実行
        driver = webdriver.Chrome(options=options)
        
        driver.get("https://slbsso.meijo-u.ac.jp/opensso/sso.jsp?app=ccmoon")
        cookie_selenium = [
            {
                "domain":   "meijo-u.ac.jp",
                "name":     'iPlanetDirectoryPro',
                "value":    tokens.tokenId
            },
        ]
        for cookie in cookie_selenium:
            driver.add_cookie(cookie)
        driver.get("https://slbsso.meijo-u.ac.jp/opensso/sso.jsp?app=ccmoon")
        cs = driver.get_cookies()
        cookies = {}
        for cookie in cs:#requestsでも使えるようにする．
            cookies[cookie["name"]] = cookie["value"]
        while "webtop" not in driver.current_url:
            time.sleep(0.1)
        driver.close()
        return cookies
    def set_printformat(self,format=_defaultformat):
        self.printformat = format
    def get_defaultformat(self):
        return self._defaultformat
    def set_pdfdata(self,path):
        with open(path,"rb") as f:
            self.printdatapath = path