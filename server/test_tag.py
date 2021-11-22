import datetime
import json
import pytest
from jsonpath import jsonpath
import requests
from server.tag import Tag

  # 统一管理标签接口


# todo：与底层具体的实现框架代码耦合严重，无法适应变化，比如公司切换了协议，比如使用pb dubbo
# todo：代码冗余，需要封装
# todo：无法清晰的描述业务
# todo：使用jsonpath表达更灵活的递归查找（建议数据小的时候使用，数据大会比较慢）

class TestTag: # 将所有用例放在类里面
    def setup_class(self):
        self.tag = Tag()

    @pytest.mark.parametrize("tag_id,tag_name", [
        ["etO63HBwAAgRCKKH54XfbpUZY2t76NIw","tag1_dnn45"],
        ["etO63HBwAAgRCKKH54XfbpUZY2t76NIw","tag1_中文"],
        ["etO63HBwAAgRCKKH54XfbpUZY2t76NIw","tag1[中文]"]
    ]) # 装饰器里面，key= value如：tag_id = etO63HBwAAgRCKKH54XfbpUZY2t76NIw # pytest参数化的方法
    def test_tag_list(self,tag_id,tag_name):
        # group_name = "python14" 这个没有用到，可以删掉
        tag_name = tag_name + str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
        # tag = Tag() # 原来这里写的是token，现在token已经被封装到tag.py里面，现在需要用token，所以需要从tag.py里面去调用

        r = self.tag.list() # 原来这里写的是list，现在需要用list，所以需要从tag.py里面去调用
        # list会返回r的结果；r是tag.py文件里面return出来的r给到这里面的r
        r = self.tag.update(tag_id= tag_id,tag_name= tag_name) # 原理这里是写的修改的
        r = self.tag.list()

       #  tags = [
       #     tag
       #     for group in r.json()["tag_group"] if group["group_name"] == group_name
       #     for tag in group["tag"] if tag["name"] == tag_name
       # ]

        # print(jsonpath(r.json(),f"$..[?(@.name=='{tag_name}')]"))
        assert jsonpath(r.json(),f"$..[?(@.name=='{tag_name}')]") [0] ['name'] == tag_name
        # assert tags != []
    def test_tag_list_fail(self):   # 断言错误的用例
        pass
        # 这个是存放异常代码的函数
    def test_tag_list(self):
        # "group_id": "etO63HBwAANNpRaRpYT2CrwaIrXsJ7RA"
        # "id": "etO63HBwAAsxXlOK6xDkNRr48Hi6o_pw"
        self.tag.list()


    def test_tag_add(self):
        group_name="TMP00123" #这里多打了个逗号导致报错 以后再不细心我要打你了
        tag=[{"name": "TAG_1"},{"name": "TAG_2"},{"name": "TAG_3"},]
        self.tag.add(group_name=group_name, tag=tag)

    def test_tag_delete(self):
        self.tag.delete()