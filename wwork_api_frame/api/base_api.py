#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

# @Description:
# @Author : 
# @Time : 2021/10/12 16:22

import re

import jsonpath
import requests

from api_frame_study.common.helper import *

project_path = get_project_path()
conf_file = os.path.join(project_path, "config/config.ini")
host = read_conf(conf_file, "WWork", "host")
api_file = os.path.join(project_path, "data/login_api.yaml")

yaml_api_file = os.path.join(project_path, "data/get_access_token_api.yaml")
extract_data_file = os.path.join(project_path, "data/extract_data.yaml")


class BaseApi:
    def __init__(self):
        self.session = requests.session()  # 实例化session对象，保持后续发送的所有请求之间cookies
        self.method = None
        self.url = None
        self.kwargs = None

    def api_info_check(self, api_info):
        api_keys = api_info.keys()
        request_keys = api_info['request'].keys()
        if "request" in api_keys and "validate" in api_keys:
            if "method" in request_keys and "path" in request_keys:
                self.method = api_info['request']['method']
                self.url = host + api_info['request']['path']
                del api_info['request']['method'], api_info['request']['path']
                self.kwargs = api_info['request']
                # print(self.kwargs)
                try:
                    for key, value in self.kwargs.items():
                        if key in ['params', 'data', 'json']:
                            for i in self.kwargs[key].keys():
                                if self.kwargs[key][i] == 'None':
                                    self.kwargs[key][i] = None
                except:
                    pass
            else:
                print("接口请求缺少必须的关键字method或url")
        else:
            print("接口请求缺少必须关键字request或validate")

    def send_request(self, api_info, extract_param_file=None):
        self.api_info_check(api_info)
        res = self.session.request(method=self.method, url=self.url, **self.kwargs)
        status_code = res.status_code
        print(res.json())
        self.extract_params(api_info, extract_param_file, res)
        validate = api_info['validate']
        self.validate_result(validate, res, status_code)

    def complete_request_info(self, test_data, api_template, param_file):
        """
        替换测试数据yaml文件中${}和接口测定时用力模板中${}和$，形成测试用例数据
        :param test_data: 测试用例数据，可能包含${}动态参数
        :param api_template: 接口测试模板数据，可能包含${}和$
        :param param_file: 接口关联参数文件
        :return: 替换后的测试用例数据
        """
        test_data = self.complete_test_data(test_data)  # 替换测试数据文件中的动态参数${}

        api_template = self.complete_api_template(api_template, param_file)  # 替换测试模板中的关联参数${}
        test_cases = template_replace(api_template, test_data)  # 替换测试用例模板中的$参数
        return test_cases

    @staticmethod
    def complete_test_data(case_data, module_name='debug_talk'):
        """
        运用热加载模块，替换测试用例中${}，完整测试用例数据
        :param case_data: 测试用例数据
        :param module_name: 热加载模块名称，默认debug_talk,可根据需要自定义其他模块进行热加载
        :return: 完整的测试用例数据，以字典格式返回
        """
        if case_data and isinstance(case_data, dict):
            case_data_str = json.dumps(case_data)  # 将数据统一转换成json字符串
        else:
            case_data_str = case_data
        if '${' in case_data_str:
            case_data_str = str_replace(case_data_str, module_name)
        else:
            pass
        return json.loads(case_data_str)

    @staticmethod
    def complete_api_template(api_template, file_name):
        """
        运用数据关联中的参数，替换测试用例中${}，完整接口模板信息
        :param api_template: 接口信息模板
        :param file_name: 接口关联数据文件 yaml文件
        :return: 完整的测试用例数据，以字典格式返回
        """
        if api_template and isinstance(api_template, dict):
            api_template_str = json.dumps(api_template)  # 将数据统一转换成json字符串
        else:
            api_template_str = api_template
        if '${' in api_template_str:
            api_template_str = str_replace(api_template_str, file_name)
        else:
            pass
        return api_template_str

    @staticmethod
    def extract_params(api_info, extract_param_file, res):
        """
        提取响应中的需要关联的参数
        :param api_info: 接口信息，获取extract关键字，如果有extract关键字，需要提取关联参数，在通过extract二级关键字获取需要提取的参数
        :param extract_param_file: yaml格式关联参数文件
        :param res: 响应结果
        :return:
        """
        if api_info.get('extract'):  # 判断接口是否需要提取参数
            for key, value in api_info.get('extract').items():  # 判断参数提取方式如果包含'(.*?)'或'(.+?)'，说明是正则表达式提取
                if '(.*?)' in value or '(.+?)' in value:
                    try:
                        reg_value = re.search(value, res.text)  # 正则表达式提取value
                        if reg_value:    # 如果匹配到值
                            print(f"提取参数{key}")
                            extract_data = {key: reg_value.group(1)}   # 提取出匹配到的值
                            yaml_data = read_yaml(extract_param_file)   # 读取关联参数文件内容
                            if yaml_data:   # 判断关联参数文件是否为空，如果为空，直接写入，不过不为空，更新里面的键
                                print(f"更新关联参数{extract_data}")
                                yaml_data.update(extract_data)
                                write_yaml(extract_param_file, yaml_data)
                            else:
                                print(f"更新关联参数{extract_data}")
                                write_yaml(extract_param_file, extract_data)
                    except:
                        print(f"响应中没有匹配到{key},无法提取此参数！")
                else:  # 直接提取
                    try:
                        extract_data = {key: res.json()[value]}     # 直接通过响应字段提取
                        yaml_data = read_yaml(extract_param_file)
                        if yaml_data:
                            print(f"更新关联参数{extract_data}")
                            yaml_data.update(extract_data)
                            write_yaml(extract_param_file, yaml_data)
                        else:
                            print(f"更新关联参数{extract_data}")
                            write_yaml(extract_param_file, extract_data)
                    except:
                        print(f"响应中没有匹配到{key},无法提取此参数！")

    @staticmethod
    def validate_result(expect_res, actual_res, status_code):
        """
        断言响应结果
        :param expect_res: 预期的响应结果
        :param actual_res: 实际的响应结果
        :param status_code: 响应状态码
        :return:
        """
        flag = 0
        for expect in expect_res:
            for key, value in expect.items():
                if key == "equals":
                    for assert_key, assert_value in value.items():
                        # print(assert_key, assert_value)
                        if assert_key == "status_code":
                            if status_code != assert_value:
                                flag = flag + 1
                                print(f"断言失败{assert_key}不等于{assert_value}！")
                        else:
                            res_list = jsonpath.jsonpath(actual_res.json(), f'$..{assert_key}')
                            if res_list:
                                res_list = [str(i) for i in res_list]
                                if assert_value not in res_list:
                                    flag = flag + 1
                                    print(f"断言失败{assert_key}不等于{assert_value}！")
                            else:
                                flag = flag + 1
                                print(f"断言失败，响应结果中不存在{assert_key}")
                elif key == "contains":
                    if value not in json.dumps(actual_res.json()):
                        flag = flag + 1
                        print(f"断言失败，响应结果中不包含字符串{value}")
                else:
                    print("框架暂不支持此断言方式！")
        assert flag == 0

    @staticmethod
    def get_text_jsonpath(res, key):
        """
        适用场景：请求响应结果是json数据结构
        通过jsonpath提取请求响应中需要校验的字段
        响应结果不是标准的key,value的形式，value为list的情况处理
        将res文本转换成json，通过jsonpath解析获得指定Key的value
        :param res: 请求响应对象
        :param key: 需要提取的用于校验的字段
        :return: 返回字段的值，如果只有一个值，返回该值string类型，如果有多个值，返回一个list
        """
        if res is not None:
            try:
                if not isinstance(res, dict):  # 如果响应不是python对象格式，反序列化为python数据对象（列表，元祖，字典）
                    res = json.loads(res)
                value = jsonpath.jsonpath(res, '$..{0}'.format(key))  # jsonpath获取的结果是一个list
                if value:
                    if len(value) == 1:  # 如果只有1个值，则返回该值
                        return value[0]
                    return value  # 如果有多个值，返回list
            except Exception as e:
                return e
        else:
            return None

    @staticmethod
    def get_text_reg(res, reg_exp):
        """
        适用场景：请求的响应是xml格式
        通过正则表达式提取请求响应中需要校验的字段
        :param res: 请求响应对象
        :param reg_exp: 正则表达式
        :return:
        """
        obj = re.search(reg_exp, res)  # 如果匹配到值，则返回值，如果没有匹配到值，返回None
        if obj:
            value = obj.group(1)
            return value
        else:
            return None
