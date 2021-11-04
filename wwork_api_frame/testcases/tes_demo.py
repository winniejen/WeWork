#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

# @Description:request基本运用与封装思路
# @Author : jwy
# @Time : 2021/10/17 14:46
import json
import os

import pytest
import requests

from api_frame_study.common.helper import get_project_path, read_conf, read_yaml

project_path = get_project_path()
conf_file = os.path.join(project_path, "config/config.ini")
host = read_conf(conf_file, "WWork", "host")
test_data_file = os.path.join(project_path, "data/test_demo.yaml")


class TestDemo:
    access_token = None

    @pytest.mark.parametrize("test_data",read_yaml(test_data_file))
    def test_gettoken(self,test_data):
        # 数据准备
        corpid = test_data['corpid']
        corpsecret = test_data['corpsecret']
        url = host + "/cgi-bin/gettoken"
        params = {
            "corpid": corpid,
            "corpsecret": corpsecret
        }
        # 发送请求
        res = requests.get(url, params=params)
        access_token = res.json().get("access_token")
        if access_token:
            TestDemo.access_token = access_token
        # 响应结果
        print(res.json())
        assert res.status_code == 200
        assert test_data['errcode'] == res.json()['errcode']
        assert test_data['errmsg'] in res.json()['errmsg']

    # def test_create_department(self):
    #     # 数据准备
    #     url = f"{host}/cgi-bin/department/create?access_token={TestDemo.access_token}"
    #     data = {
    #         "name": "广州研发",
    #         "name_en": "RDGZ",
    #         "parentid": 1,
    #         "order": 1,
    #         "id": 2
    #     }
    #     # 发送请求
    #     res = requests.post(url=url, data=json.dumps(data))
    #     # 响应结果
    #     print(res.json())


if __name__ == '__main__':
    pytest.main(['-vs', 'test_demo.py'])
