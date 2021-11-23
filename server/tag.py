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

    def add(self,group_name,tag,**kwargs):
        print(group_name,tag)
        r = requests.post("https://qyapi.weixin.qq.com/cgi-bin/externalcontact/add_corp_tag",
            params={"access_token": self.token},
            json={"group_name": group_name, "tag": tag, **kwargs}
        )
        print(json.dumps(r.json(),indent=2))  # indent=2 缩进字符
        return r

    def before_add(self,group_name,tag,**kwargs):
        r = self.add(group_name,tag,**kwargs)
        # 如果删除的元素已经存在
        if r.status_code == 200 and r.json()["errcode"] == "40071":
        # 查询元素是否存在，如果不存在，报错
            for group in self.list().json()["tag_group"]:
                if group_name not in group:
                    print("group name not in group")
                    return False

        # 如果存在，直接删除
            for group in self.list().json()["tag_group"]:
                if group_name in group:
                    print("删除成功")
                    return r




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
        print(json.dumps(r.json(),indent=2))
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
        print(json.dumps(r.json(), indent=2))
        return r

    # 查询tag_id,然后删除tag_id
    def delete_group(self,group_id):
        r = requests.post(
            "https://qyapi.weixin.qq.com/cgi-bin/externalcontact/del_corp_tag",
            params = {"access_token": self.token},
            json = {"group_id": group_id
                    }
        )
        print(json.dumps(r.json(), indent=2))
        return r

    def delete_tag(self,tag_id):
        r = requests.post(
            "https://qyapi.weixin.qq.com/cgi-bin/externalcontact/del_corp_tag",
            params = {"access_token": self.token},
            json = {
                    "tag_id": tag_id
                    }
        )
        print(json.dumps(r.json(), indent=2))
        return r
