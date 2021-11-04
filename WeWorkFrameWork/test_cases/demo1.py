#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

# @Description:
# @Author : 
# @Time : 2021/8/25 21:47

from functools import wraps
import logging
# 1. 定义一个日志装饰器

# 日志文件的配置
from util.log import Log

logging.basicConfig(
    level=logging.DEBUG,
    filename="message.txt",
    filemode="a",
    format="%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s"
)

my_logger = Log()

my_logger.logger.info("测试通过")


def logger(func):
    """插入日志的装饰器"""
    # @wraps(func)，用来保留func函数原有的函数名和帮助文档
    @wraps(func)
    def wrapper(*args, **kwargs):     # args, kwargs为形参，args是元组，kwargs是字典
        logging.debug("%s函数开始执行" % (func.__name__))
        result = func(*args, **kwargs)  # args, kwargs为实参，*args, **kwargs为解包
        logging.debug("%s函数结束执行" % (func.__name__))
        return result
    return wrapper