#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

# @Description:部门管理接口包括创建部门，更新部门，删除部门，获取部门列表
# @Author : 
# @Time : 2021/10/14 17:56

# 导包
from api_frame_study.api.base_api import BaseApi
from api_frame_study.common.helper import *

project_path = get_project_path()  # 获取项目路径
# 获取接口信息
department_api = read_yaml(os.path.join(project_path, "data/department_api.yaml"))
create_department_api = department_api['create_department']
update_department_api = department_api['update_department']
get_department_api = department_api['get_department']
delete_department_api = department_api['delete_department']
# 关联参数提取文件
extract_data_file = os.path.join(project_path, "data/extract_data.yaml")


class DepartmentApi(BaseApi):
    def create_department(self, req_data):
        """
        创建部门接口
        :param req_data: 创建部门接口模板中，需要$替换的变量
        :return:
        """
        # 替换$后，完整的接口请求数据包括method,url,params等信息
        req_data = self.complete_request_info(req_data, create_department_api, extract_data_file)
        # print(req_data)
        self.send_request(req_data, extract_data_file)  # 发送请求,并将关联参数department_id保存到extract_data_file中

    def update_department(self, req_data):
        """
        更新部门接口
        :param req_data: 更新部门接口模板中，需要$替换的变量
        :return:
        """
        # 替换$后，完整的接口请求数据包括method,url,params等信息
        print(req_data)
        req_data = self.complete_request_info(req_data, update_department_api, extract_data_file)
        print(req_data)
        # print(req_data)
        self.send_request(req_data)

    def get_department(self, req_data):
        """
        获取部门列表接口
        :param req_data: 获取部门列表模板中，需要$替换的变量
        :return:
        """
        # 替换$后，完整的接口请求数据包括method,url,params等信息
        req_data = self.complete_request_info(req_data, get_department_api, extract_data_file)
        # print(req_data)
        self.send_request(req_data)

    def delete_department(self, req_data):
        """
        删除部门接口
        :param req_data: 删除部门接口模板中，需要$替换的变量
        :return:
        """
        # 替换$后，完整的接口请求数据包括method,url,params等信息
        req_data = self.complete_request_info(req_data, delete_department_api, extract_data_file)
        # print(req_data)
        self.send_request(req_data)