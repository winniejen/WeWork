#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

# @Description:解析yaml文件
# @Author : jwy
# @Time : 2021/8/24 11:12
import os

import yaml

from util.helper import projet_path


def read_yaml(file_name):
    """
    解析yaml文件数据
    :param file_name:yaml文件路径名称
    :return:
    """
    # 增加try,except容错处理
    try:
        # 打开yaml文件
        with open(file_name, mode='r', encoding="utf-8") as f:
            yaml_data = yaml.safe_load(f)  # 加载yaml数据
            return yaml_data
    except FileNotFoundError:
        print(f"{file_name}不存在！")
        return None


def parse_yaml(data_file):
    """
    读取yaml文件数据
    :param data_file: 文件名称
    :return: yaml列表信息，return_value[0]为接口描述的通用信息，return_value[1:]返回pytest参数化的测试数据列表格式
    """
    return_value = []
    with open(data_file, 'r', encoding='utf-8') as f:
        yaml_data = yaml.safe_load(f)
    test_case = yaml_data['test_case']
    for item in test_case:
        return_value.append(tuple(item.values()))
    print(return_value)
    return return_value



# 测试代码
if __name__ == '__main__':
    # add_members_test_data_yaml = os.path.abspath(os.path.join(projet_path(), "data/add_members_test_data.yaml"))
    # add_members_locator_yaml = os.path.abspath(os.path.join(projet_path(), "data/add_members_locator.yaml"))
    # print(add_members_test_data_yaml)
    # test_data = read_yaml(add_members_test_data_yaml)
    # print(test_data)
    # print(add_members_locator_yaml)
    # locator_data = read_yaml(add_members_locator_yaml)
    # print(locator_data)
    add_members_testcases = os.path.abspath(os.path.join(projet_path(), "data/add_members_testcases.yaml"))
    parse_yaml(add_members_testcases)
