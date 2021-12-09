import json

import requests


class BaseApi:
    params = {}
    def __init__(self):
        self.token = self.get_token() # 初始化token；get_token()为啥要加self是因为：调用这个类中的get_token方法
         # shift+tab  往前缩进    # 光标放在引用函数地方，CTRL+鼠标左键，跳转另一个页面

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
        raw_data = json.dumps(kwargs)  # yaml文件的原始数据  json.dumps数据类型转换成json格式的字符串
        for key, value in self.params.items():
            value = str(value)
            raw_data = raw_data.replace("${"+key+"}", value)  # 对yaml文件进行处理
        kwargs = json.loads(raw_data)
        r = requests.request(**kwargs)
        print(json.dumps(r.json(), indent=2))
        return r

