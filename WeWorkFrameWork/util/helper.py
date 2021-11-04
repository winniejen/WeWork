#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

# @Description:获取项目路径
# @Author : jwy
# @Time : 2021/8/24 11:29

import os


def projet_path():
    """
    获取当前项目工程的绝对路径
    :return:
    """
    dir_path = os.path.dirname(__file__)  # 获取当前文件夹路径
    project_path = os.path.abspath(os.path.join(dir_path, "../"))  # 获取当前文件夹路径的父路径
    return project_path


# 测试代码
if __name__ == '__main__':
    print(projet_path())
