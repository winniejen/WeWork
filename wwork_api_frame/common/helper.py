#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

# @Description:
# @Author : 
# @Time : 2021/10/12 16:30
import json
import os
from configparser import ConfigParser
from string import Template
import importlib
import yaml


def get_project_path():
    """
    获取项目路径
    :return: 返回项目根目录
    """
    # abspath(path)返回绝对路径 dirname(）返回文件路径 getcwd()当前运行代码路径
    return os.path.abspath(os.path.dirname(os.getcwd()))


def read_yaml(file_path):
    """
    读取yaml文件数据
    :param file_path: yaml文件路径
    :return: yaml文件数据
    """
    with open(file_path, "r") as f:  # 以只读的方式打开文件
        data = yaml.safe_load(f)    # 读取yaml文件数据
        return data   # 返回yaml数据


def write_yaml(file_name, data):
    """
    写入数据到yaml文件
    :param file_name: Yaml文件名称
    :param data: 写入的数据
    :return:
    """
    with open(file_name, encoding='utf-8', mode='w') as f:
        yaml.safe_dump(data, stream=f, allow_unicode=True)


def clear_yaml(file_name):
    """
    清除yaml文件的数据
    :param file_name: yaml文件名称
    :return:
    """
    with open(file_name, encoding='utf-8', mode='w') as f:
        f.truncate()


def read_conf(file_path, section, option):
    """
    读取.ini配置文件中指定section下，指定的option的值
    :param file_path: 配置文件路径
    :param section: 配置文件section 一级目录
    :param option: section下的option 二级目录
    :return: option的值
    """
    cf = ConfigParser()  # 创建配置文件对象
    cf.read(file_path)  # 读取配置文件
    value = cf.get(section, option)  # 获取一级目录下，二级目录的值
    return value


def template_replace(template, data: dict):
    """
    利用string库中Template类替换数据
    :param template: string类型模板数据
    :param data: 字典格式替换参数 {key1:value1,key2:value2}
    :return: 字典类型数据
    """
    return json.loads(Template(template).substitute(data))


def str_replace(data_str, name):
    """
    替换数据中${}包裹的值
    :param data_str: 需要替换的字符串格式数据
    :param name: 替换yaml文件名称或模块名称
    :return:将${}替换后的数据，数据类型与data相同
    """
    if data_str and "${" in data_str:
        for param in range(1, data_str.count("${") + 1):
            try:
                start_index = data_str.index("${")
                end_index = data_str.index("}", start_index)
                old_value = data_str[start_index:end_index + 1]
                extract_key = data_str[start_index + 2:end_index]
            except:
                old_value = None
                extract_key = None
            if extract_key:
                if "(" and ")" in extract_key:
                    try:
                        # 动态导入api_frame_study.common包下的value模块
                        module_name = f"api_frame_study.common.{name}"
                        import_module = importlib.import_module(module_name)
                        new_value = eval(f"import_module.{extract_key}")
                    except:
                        new_value = None
                        print(f"导入{name}模块，执行{extract_key}失败！")
                else:
                    try:
                        new_value = read_yaml(name)[extract_key]   # 获取yaml文件中的extract_key的值
                    except:
                        new_value = None  #
                        print(f"在{name}中，未获取到{extract_key}的值！")
                data_str = data_str.replace(old_value, str(new_value))
    else:
        pass
    return data_str
