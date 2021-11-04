#!/usr/bin/env python 

# -*- coding: utf-8 -*- 
# 
# @Description:企业微信个人首页HomePage类封装
# @Author : jwy
# @Time : 2021/8/23 17:26
import allure

from page_objects.common_operations import CommonOperations


class HomePage(CommonOperations):
    _add_member_locator = ["css selector", ".ww_indexImg_AddMember"]   # 添加成员元素定位
    _goto_contacts_locator = ['css selector', "#menu_contacts"]   # 通讯录元素定位
    _homepage_url = "https://work.weixin.qq.com/wework_admin/frame#index"  # 首页url

    def get_homepage_url(self):
        """
        打开通讯录页面
        :return:
        """
        self.get_url(self._homepage_url)
        return self

    @allure.step("点击添加成员")
    def add_member_in_homepage(self):
        """
        在企业微信个人首页，点击添加成员
        :return:页面跳转到添加成员页面，返回添加成员页面对象
        """
        self.wait_time(5)  # 强制等待5s
        self.click(*self._add_member_locator)  # 点击添加成员
        from page_objects.add_member_page import AddMemberPage  # 导包放在方法里面，解决循环调用问题
        return AddMemberPage(self.driver)  # 链式调用

    @allure.step("点击通讯录")
    def goto_contacts(self):
        """
        在企业微信个人首页，点击通讯录
        :return:页面跳转到通讯录页面
        """
        self.wait_time(5)  # 强制等待5s
        self.click(*self._goto_contacts_locator)  # 点击添加成员
        from page_objects.contacts_page import ContactsPage  # 导包放在方法里面，解决循环调用问题
        return ContactsPage(self.driver)  # 链式调用


# 测试代码
if __name__ == '__main__':
    user_locator = ["id", "username"]  # 姓名定位方式和定位表达式
    home_page = HomePage()  # 创建一个HomePage类实例
    home_page.open_browser("Chrome")  # 打开浏览器
    home_page.get_homepage_url()   # 打开homepage页面
    # home_page.add_member_in_homepage()  # 点击添加成员
    home_page.goto_contacts()  # 点击通讯录
