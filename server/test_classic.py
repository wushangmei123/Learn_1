import datetime
import json
import requests


# todo：与底层具体的实现框架代码耦合严重，无法适应变化，比如公司切换了协议，比如使用pb dubbo
# todo：代码冗余，需要封装
# todo：无法清晰的描述业务
# todo：使用jsonpath表达更灵活的递归查找（建议数据小的时候使用，数据大会比较慢）





def test_tag_list():
    corpid = 'ww4590ee5fb4cdc54b'
    corpsecret = 'D465rLSeMJmOlveJXP21pJ-drF_O36sH6OSy2DskHxo'
    r = requests.get(
        'https://qyapi.weixin.qq.com/cgi-bin/gettoken',
        params = {'corpid':corpid,'corpsecret':corpsecret}
    )

    token = r.json()['access_token']

    r = requests.post(
        'https://qyapi.weixin.qq.com/cgi-bin/externalcontact/get_corp_tag_list',
        params = {
            "access_token": token
        }, # params传参
        json = {
            "tag_id": [],
            "group_id": []
        })

    print(json.dumps(r.json(),indent = 2))  # 调试数据
    # 打印json()信息  设置indent格式，encoding打印编码使用格式
    # "errmsg": "Warning: wrong json format. invalid access_token"
    assert r.status_code == 200
    assert r.json()['errcode'] == 0

    tag_name = "tag1_dnn45" + str(datetime.datetime.now().strftime("%Y%m%d-%H%M"))
    r = requests.post(
        'https://qyapi.weixin.qq.com/cgi-bin/externalcontact/edit_corp_tag',
        params = {
            "access_token": token
        },
        json = {
            "id": "etO63HBwAAgRCKKH54XfbpUZY2t76NIw",
            "name": tag_name
        }
    )
    assert r.status_code == 200
    assert r.json()['errcode'] == 0
    r = requests.post(
        'https://qyapi.weixin.qq.com/cgi-bin/externalcontact/get_corp_tag_list',
        params={
            "access_token": token},
        json={
            'tag_id': [],
            'group_id': []
        }
    )

    tags = [
        tag
        for group in r.json()["tag_group"] if group["group_name"] == "python14"
        for tag in group["tag"] if tag["name"] == tag_name
    ]
    # jsonpath(f"$..[?(@.name='{tag_name}')]")    # 不太懂，17：36
    assert tags != []

