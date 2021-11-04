#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

# @Description: 获取access_token接口测试用例
# @Author : jwy
# @Time : 2021/10/12 16:34
import os

import pytest

# 导包
from api_frame_study.api.get_access_token import GetAccessToken
from api_frame_study.common.helper import get_project_path, read_yaml

project_path = get_project_path()   # 获取项目路径

# 获取接口测试数据
get_access_token_data = read_yaml(os.path.join(project_path, "data/get_access_token_data.yaml"))


class TestGetAccessToken:
    get_access_token_api = GetAccessToken()   # 实例化接口

    @pytest.mark.parametrize("test_data", get_access_token_data)  # 参数化测试数据
    def test_get_access_token(self, test_data):
        self.get_access_token_api.get_access_token(test_data)  # 测试获取access_token接口


if __name__ == '__main__':
    pytest.main(['-vs', 'test_get_access_token.py'])
