#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

# @Description: 部门管理模块测试用例
# @Author : jwy
import os

import pytest

# 导包
import requests

from api_frame_study.api.department_api import DepartmentApi
from api_frame_study.common.helper import get_project_path, read_yaml

project_path = get_project_path()  # 获取项目路径

# 读取测试数据
create_department_data = read_yaml(os.path.join(project_path, "data/create_department_data.yaml"))
update_department_data = read_yaml(os.path.join(project_path, "data/update_department_data.yaml"))
get_department_data = read_yaml(os.path.join(project_path, "data/get_department_data.yaml"))
delete_department_data = read_yaml(os.path.join(project_path, "data/delete_department_data.yaml"))


class TestDepartment:
    department_api = DepartmentApi()  # 实例化接口

    @pytest.mark.parametrize("test_data", create_department_data)  # 参数化测试数据
    def test_create_department(self, test_data):
        self.department_api.create_department(test_data)  # 测试创建部门接口

    @pytest.mark.parametrize("test_data", update_department_data)  # 参数化测试数据
    def test_update_department(self, test_data):
        self.department_api.update_department(test_data)  # 测试更新部门接口

    @pytest.mark.parametrize("test_data", get_department_data)  # 参数化测试数据
    def test_get_department(self, test_data):
        self.department_api.get_department(test_data)   # 测试获取部门列表接口

    @pytest.mark.parametrize("test_data", delete_department_data)  # 参数化测试数据
    def test_delete_department(self, test_data):
        self.department_api.delete_department(test_data)  # 测试删除部门接口


if __name__ == '__main__':
    pytest.main(['-vs', 'test_department.py'])
