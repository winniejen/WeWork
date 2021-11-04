#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

# @Description: 获取get_access_token接口
# @Author : jwy
# @Time : 2021/10/19 15:30

# 导包
from api_frame_study.api.base_api import BaseApi
from api_frame_study.common.helper import *

project_path = get_project_path()  # 获取项目路径
extract_data_file = os.path.join(project_path, "data/extract_data.yaml")  # 关联参数yaml文件，用于将关联参数写入文件中
# 读取yaml文件接口信息
get_access_token_api = read_yaml(os.path.join(project_path, "data/get_access_token_api.yaml"))['get_access_token']


class GetAccessToken(BaseApi):
    def get_access_token(self, req_data):
        """
        获取access_token接口
        :param req_data: 接口信息模板中$标识的待替换的数据
        data/get_access_token_api.yaml示例
            get_access_token:  # 获取access_token接口
                  request:
                    method: get
                    path: /cgi-bin/gettoken
                    params:
                      corpid: $corpid
                      corpsecret: $corpsecret
                  # json表达式提取，正则表达式提取
                  extract:
                    access_token: '"access_token":"(.*?)",'
                  validate:
                    - equals: {status_code: 200}
                    - equals: {errcode: $errcode}
                    - contains: $errmsg
        """
        req_data = self.complete_request_info(req_data, get_access_token_api, extract_data_file)  # 完善接口请求信息
        self.send_request(req_data, extract_param_file=extract_data_file)  # 发送请求，将关联参数写入yaml文件中
