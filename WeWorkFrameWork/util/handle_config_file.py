#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

# @Description:解析.ini配置文件
# @Author : jwy
# @Time : 2021/8/24 14:00
import os
from configparser import ConfigParser

from util.helper import projet_path


class HandleConfigFile:
    def __init__(self, file_name):
        """
        构造函数，创建config文件实例对象，读取配置文件
        :param file_name:
        """
        self.cf = ConfigParser()  # 创建ConfigParser类实例，该类提供读取配置文件的方法
        self.cf.read(file_name)  # 读取配置文件

    def get_items_section(self, section_name):
        """
        获取配置文件中指定section下的所有option键值对
        返回字典类型的值
        注意：
        使用self.cf.items(section_name)获取到的配置文件中options内容均被换成小写
        :param section_name: section_name
        :return:
        """
        option_dict = dict(self.cf.items(section_name))
        return option_dict

    def get_option_value(self, section_name, option_name):
        """
        获取指定section下的指定option值
        :param section_name: section_name
        :param option_name: option_name
        :return:
        """
        return self.cf.get(section_name, option_name)


# 测试代码
if __name__ == '__main__':
    config_file_name = os.path.join(projet_path(), "config.ini")
    conf_file = HandleConfigFile(config_file_name)
    print(conf_file.get_items_section("TEST_URL"))
    print(conf_file.get_option_value("TEST_URL", "home_page_url"))
