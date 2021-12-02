import json

import requests


class BaseApi:
    def __init__(self):
        self.token = self.get_token() # 初始化token；get_token()为啥要加self是因为：调用这个类中的get_token方法

    def get_token(self):
        corpid = 'ww4590ee5fb4cdc54b'
        corpsecret = 'D465rLSeMJmOlveJXP21pJ-drF_O36sH6OSy2DskHxo'
        data ={"method": "get",
               "url": "https://qyapi.weixin.qq.com/cgi-bin/gettoken",
               "params": {'corpid': corpid, 'corpsecret': corpsecret}
               }
        r = self.send(data)
        # r = requests.get(
        #     'https://qyapi.weixin.qq.com/cgi-bin/gettoken',
        #     params={'corpid': corpid, 'corpsecret': corpsecret}
        # )
        token = r.json()['access_token']
        return token

    def send(self,kwargs):
        r = requests.request(**kwargs)
        print(json.dumps(r.json(),indent=2))
        return r

