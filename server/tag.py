import datetime
import json
import subprocess

import requests

from server.base_api import BaseApi


class Tag(BaseApi):   # 继承父类BaseApi
    def __init__(self):     # __init__构造函数
        super().__init__()     # super是调用父类里面的__init__方法

    def find_group_id_by_name(self, group_name):
            # 查询元素是否存在，如果不存在，报错
        for group in self.list().json()["tag_group"]:
            if group_name in group["group_name"]:
                # delete_1 = group["group_id"]
                # print(delete_1)
                # return delete_1
                return group["group_id"]    # 方法二
        print("group name not in group")
        return ""

    def add_and_detect(self, group_name, tag, **kwargs):
        r = self.add(group_name, tag, **kwargs)
        # 如果删除的元素已经存在
        if r.json()["errcode"] == 40071:
            group_id = self.find_group_id_by_name(group_name)
            if not group_id:
                return ""
            self.delete_group([group_id])
            self.add(group_name,tag,**kwargs)
        result = self.find_group_id_by_name(group_name)
        if not result:
            print("add not success")
        return result


    def add(self,group_name,tag,**kwargs):
        data = {
            "method": "post",
            "url": "https://qyapi.weixin.qq.com/cgi-bin/externalcontact/add_corp_tag",
            "params":{"access_token": self.token},
            "json": {"group_name": group_name, "tag": tag, **kwargs}
        }
        r = self.send(data)
        return r

        # print(group_name,tag)
        # r = requests.post("https://qyapi.weixin.qq.com/cgi-bin/externalcontact/add_corp_tag",
        #     params={"access_token": self.token},
        #     json={"group_name": group_name, "tag": tag, **kwargs}
        # )
        # print(json.dumps(r.json(),indent=2))  # indent=2 缩进字符


    # def before_1_add(self,group_name,tag,**kwargs): # 添加之前的验证
    #     r = self.add(group_name,tag,**kwargs)
    #     # 如果要添加的元素已经存在
    #     if r.status_code == 200 and r.json()["errcode"] == "40071":  # r.json指的是响应结果，返回的结果
    #     # 查询元素是否存在，如果不存在，报错
    #         for group in self.list().json()["tag_group"]:  # group去遍历self.list（）查询接口响应中tag_group对应的值
    #             if group_name not in group["goup_name"]:
    #                 print("group name not in group")
    #                 return False
    #     # 如果存在，直接删除
    #             else:
    #                 for group_1 in self.list().json()["tag_group"]: # group_1去遍历self.list（）查询接口响应中tag_group对应的值
    #                     if group_name in group_1["group_name"]:  # 如果group_name在group_1中
    #                         delete_1 = group_1["group_id"] # 通过group_1中的group_id去获取它对应的值
    #                         # for tag_1 in  group_1["tag"]:
    #                         #     if name in tag_1["name"]:
    #                         #         delete_2=tag_1["id"]
    #                         self.delete_group(delete_1)
    #                         # self.delete_group(delete_2)
    #                         self.add(group_name,tag)
    #                         return True
    '''接口测试核心：发送请求 获取响应 对响应结果进行判断 一般会将响应结果用json形式打印出来 方便判断 
       复杂逻辑的判断：一般是通过Key去找它对应的value；如果value还是一个字典格式，继续通过key去找'''




    def list(self):   # 查询
        data = {
            "method": "post",
            "url": "https://qyapi.weixin.qq.com/cgi-bin/externalcontact/get_corp_tag_list",
            "params": {"access_token": self.token},
            "json":  {"tag_id": [],"group_id": []}
        }
        r = self.send(data)
        return r

        # r = requests.post(
        # 'https://qyapi.weixin.qq.com/cgi-bin/externalcontact/get_corp_tag_list',
        # params = {
        #     "access_token": self.token  # 已封装的部分都需要替换，所以这里调用写成self.token，而不是写成token
        # }, # params传参
        # json = {
        #     "tag_id": [],
        #     "group_id": []}
        # )
        # print(json.dumps(r.json(),indent=2))


    def update(self,tag_id,tag_name):
        data = {
            "method": "post",
            "url": "https://qyapi.weixin.qq.com/cgi-bin/externalcontact/edit_corp_tag",
            "params": {"access_token": self.token},
            "json": {"id": tag_id,"name": tag_name}
        }
        r = self.send(data)
        return r

        # r = requests.post(
        #     'https://qyapi.weixin.qq.com/cgi-bin/externalcontact/edit_corp_tag',
        #     params={
        #         "access_token": self.token
        #     },
        #     json={
        #         "id": tag_id,
        #         "name": tag_name
        #     }
        # )
        # print(json.dumps(r.json(), indent=2))
        # return r

    # 查询tag_id,然后删除tag_id
    def delete_group(self,group_id):
        data = {
            "method": "post",
            "url": "https://qyapi.weixin.qq.com/cgi-bin/externalcontact/del_corp_tag",
            "params": {"access_token": self.token},
            "json": {"group_id": group_id}
        }
        r = self.send(data)
        return r

        # r = requests.post(
        #     "c",
        #     params = {"access_token": self.token},
        #     json = {"group_id": group_id
        #             }
        # )
        # print(json.dumps(r.json(), indent=2))
        # return r

    def delete_tag(self,tag_id):
        data = {
            "method": "post",
            "url": "https://qyapi.weixin.qq.com/cgi-bin/externalcontact/del_corp_tag",
            "params": {"access_token": self.token},
            "json": {"tag_id": tag_id}
        }
        r = self.send(data)
        return r

        # r = requests.post(
        #     "https://qyapi.weixin.qq.com/cgi-bin/externalcontact/del_corp_tag",
        #     params = {"access_token": self.token},
        #     json = {
        #             "tag_id": tag_id
        #             }
        # )
        # print(json.dumps(r.json(), indent=2))
        # return r

    def group_id_exist(self, group_id):
            # 查询元素是否存在，如果不存在，报错
        for group in self.list().json()["tag_group"]:
            if group_id in group["group_id"]:
                # delete_1 = group["group_id"] # 方法一
                # print(delete_1)
                # return delete_1
                return True   # 方法二
        print("group id not in group")
        return False

    def delete_and_detect_group(self,group_ids):
        deleted_group_ids = [] # 先定义一个需要删除的列表
        r = self.delete_group(group_ids)
        if r.json()["errcode"] == 40068:
            # 如果标签不存在，就添加一个标签，将它的group_id 存储进来
            for group_id_tmp in group_ids:
                if not self.group_id_exist(group_id_tmp): # 如果要添加的元素不存在
                    # 给他添加一个元素，拿到添加元素的响应中的group_id
                    # group_id = self.add_and_detect("TMP00123",[{"name":"123"}]).json()["tag_group"]["group_id"]
                    group_id_tmp = self.add_and_detect("TMP00123", [{"name": "TAG123"}])
                    deleted_group_ids.append(group_id_tmp)
                # 如果标签存在，就将它存入标签组
                else:
                    deleted_group_ids.append(group_id_tmp)
            r = self.delete_group(deleted_group_ids)
        return r






