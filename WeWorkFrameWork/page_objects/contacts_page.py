#!/usr/bin/env python 

# -*- coding: utf-8 -*- 
# 
# @Description:通讯录页面ContactsPage类封装
# @Author : jwy
# @Time : 2021/8/23 17:26
from time import sleep

import allure

from page_objects.common_operations import CommonOperations
from util.log import log


class ContactsPage(CommonOperations):
    """
    通讯录页面类
    包含属性通讯录列表contacts_list
    包含方法添加成员add_member，获取通讯录列表get_member_list，判断添加成员成功assert_add_member_success
    """
    _get_member_list_locator = ["css selector", '#member_list td:nth-child(2)']
    _add_member_locator = ["css selector", '.js_add_member']

    @allure.step("获取通讯录列表")
    def get_member_list(self):
        """
        获取通讯录列表成员，返回通讯录list
        """
        sleep(5)
        try:
            contacts = self.get_elements(*self._get_member_list_locator)  # 获取通讯录所有成员的元素对象
            # 通过列表推导式，获取成员元素对象的text属性，保存到contacts_list中
            contacts_list = [member.text for member in contacts]
            if contacts_list:
                log.logger.info(f"通讯录成员列表：{contacts_list}")
                return contacts_list
        except Exception as e:
            log.logger.info(f"获取通讯录成员列表失败")
            raise e
        return contacts_list

    @allure.step("检查添加的成员姓名在通讯录中")
    def assert_add_member_success(self, member_name):
        """
        判断添加的成员姓名是否在通讯录中，在通讯录中，说明添加成员成功，不在通讯录中，添加成员失败
        :param member_name: 成员姓名
        :return: 添加成功返回True，添加失败返回False
        """
        try:
            contacts_list = self.get_member_list()
            print(contacts_list)
            if member_name in contacts_list:
                log.logger.info(f"成员:{member_name} 在通讯录列表{contacts_list}中")
                return True
            else:
                log.logger.error(f"成员:{member_name} 不在通讯录列表{contacts_list}中！")
                return False
        except:
            raise Exception

    @allure.step("通讯录页面，点击添加成员")
    def add_member_in_contacts(self):
        """
        通讯录页面，点击添加成员，进入到添加成员详情页面
        :return: 添加成员页面对象
        """

        self.get_elements(*self._add_member_locator)[1].click()
        from page_objects.add_member_page import AddMemberPage  # 导包放在方法里面，解决循环调用问题
        return AddMemberPage(self.driver)   # 链式调用
