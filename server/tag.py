import datetime
import json

import requests


class Tag:
    def __init__(self):
        self.token = self.get_token() # 初始化token；get_token()为啥要加self是因为：调用这个类中的get_token方法

    def get_token(self):
        corpid = 'ww4590ee5fb4cdc54b'
        corpsecret = 'D465rLSeMJmOlveJXP21pJ-drF_O36sH6OSy2DskHxo'

        r = requests.get(
            'https://qyapi.weixin.qq.com/cgi-bin/gettoken',
            params={'corpid': corpid, 'corpsecret': corpsecret}
        )
        token = r.json()['access_token']
        return token


    def add(self):
        pass

    def list(self):
        r = requests.post(
        'https://qyapi.weixin.qq.com/cgi-bin/externalcontact/get_corp_tag_list',
        params = {
            "access_token": self.token  # 已封装的部分都需要替换，所以这里调用写成self.token，而不是写成token
        }, # params传参
        json = {
            "tag_id": [],
            "group_id": []
        })
        return r

    def update(self,tag_id,tag_name):
        r = requests.post(
            'https://qyapi.weixin.qq.com/cgi-bin/externalcontact/edit_corp_tag',
            params={
                "access_token": self.token
            },
            json={
                "id": tag_id,
                "name": tag_name
            }
        )
        return r

    def delete(self):
        pass
