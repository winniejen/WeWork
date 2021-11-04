#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

# @Description:
# @Author : 
# @Time : 2021/10/14 15:27
import os
import random
from datetime import datetime

from api_frame_study.common.helper import read_yaml, get_project_path

project_path = get_project_path()  # 获取项目路径
extract_data_file = os.path.join(project_path, "data/extract_data.yaml")


def get_random_num(num_len):
    """
    获取指定长度随机数
    :param num_len: 随机数的长度
    :return: 字符串类型的随机数
    """
    # now_time = datetime.now().strftime("%Y%m%d%H%M%S")
    res = ''
    for i in range(num_len):
        value = str(random.randint(0, 9))
        res += value
    return res


def extract_data(key):
    """
    提取关联参数文件中的字段
    :param key: 需要读取的关键字
    :return:
    """
    value = read_yaml(extract_data_file).get(key)
    return value


def get_timestamp():
    """
    获取时间戳
    :return: 字符串类型的时间戳
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return timestamp


def get_special_char(char_num):
    """
    获取指定个数特殊字符
    :param char_num: 字符个数，当个数超过字符样本数量时，char_num等于样本数量
    :return: 特殊字符
    """
    char_list = [":", "*", "?", "<", ">", "|", "\\"]
    re_char = ''
    if char_num > len(char_list):
        char_num = len(char_list)
    special_char = random.sample(char_list, char_num)
    return re_char.join(special_char)

#
# char = get_special_char(8)
# print(char)

#
# value = extract_data('id')
# print(value)