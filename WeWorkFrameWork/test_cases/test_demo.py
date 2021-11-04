#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

# @Description:
# @Author : 
# @Time : 2021/8/28 19:53
from selenium import webdriver


class TestDemo:
    def test_01(self):
        driver = webdriver.Chrome()
        driver.get("")
        driver.find_element("","")