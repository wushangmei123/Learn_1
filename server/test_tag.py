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
    def setup_class(self): # setupxxx表示前置条件，它在每一个用例执行之前必须会执行一次
        self.tag = Tag()    # 实例化一个对象，调用tag.py文件中的Tag（）类方法，会先执行该类中的构造方法。
        # 实例化对象的目的，是为了调用类中封装的方法或者变量

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

    def test_tag1_list(self):
        # "group_id": "etO63HBwAANNpRaRpYT2CrwaIrXsJ7RA"
        self.tag.list()

    def test_add_tag(self): # 添加
        group_name="TMP00123"
        tag=[{"name": "TAG_1"},{"name": "TAG_21"},{"name": "TAG_31"},]
        r = self.tag.add(group_name=group_name, tag=tag)
        assert r.status_code == 200
        assert r.json()["errcode"] == 0

    def test_add_and_detect(self): # 删除后添加
        group_name = "TMP00123"
        tag = [
            {"name": "TAG_1"},
            {"name": "TAG_2"},
            {"name": "TAG_3"},
        ]
        r = self.tag.add_and_detect(group_name, tag)
        assert r

        # 如果40068，invalid tagid
        # 0. 添加tag
        # 1.删除tag 有问题
        # 2.再进去重试（重试次数：n）；手动实现，借助pytest 狗子（rerun插件）
        #a.添加一个项目
        #b.对新添加的项目在删除
        #c.查询删除是否成功

    def test_tag_delete_group(self): # 删除group_id
        self.tag.delete_group(["etO63HBwAAz7MuTilkreG9wiy8foLkjg"])

    def test_tag_delete_tag(self): # 删除tag_id
        self.tag.delete_tag(["etO63HBwAA0kzzjny_fo7A8Kq2i0zSlw"])

    def test_delete_and_detect_group(self): # 删除存在/不存在的内容
        # delete_and_detect_gorup(["xxxxxxxxx"])里面的xxx是自定义的，需要删除的内容
        r = self.tag.delete_and_detect_group(["etO63HBwAATDtabEgHG7mhimrWFuSJBA"])
        assert r.json()["errcode"] == 0


    # def setup_function():   # 测试类里面  "setup_function():每个方法之前执行"
    #
    #
    # def teardown_function():   # 测试类里面  "teardown_function():每个方法之后执行"
    #
    #

