#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

# @Description:
# @Author : 
# @Time : 2021/8/25 18:03

# 2. 装饰器，语法糖 @logger <==> login = logger(login)
import logging

from test_cases.demo1 import logger


@logger
def login(userName, passWod):
    if userName == "root" and passWod == "6666":
        print("LOGIN OK")
        logging.debug("%s LOGIN OK" % userName)
    else:
        print("LOGIN FAILED")
        logging.error("%s LOGIN FAILED" % userName)


@logger
def test():
    logging.debug("这是debug日志")


if __name__ == '__main__':
    login("root", "6666")
    test()
