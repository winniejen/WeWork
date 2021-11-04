#!/usr/bin/env python 

# -*- coding: utf-8 -*- 
# 
# @Description:添加成员页面AddMembersPage类封装
# @Author : jwy
# @Time : 2021/8/23 17:26
import allure

from page_objects.common_operations import CommonOperations
from util.log import log


class AddMemberPage(CommonOperations):
    """
    通讯录功能下，添加成员功能页面，相关的操作(功能)和属性(值)
    这只是一个demo,还有一些操作没有添加，实际项目根据需要添加，一般添加核心和常用功能，不必要为每个元素都添加
    """
    _full_name_locator = ["id", "username"]  # 姓名输入框元素定位
    _id_locator = ["id", "memberAdd_acctid"]  # 账号输入框元素定位
    _phone_locator = ["id", "memberAdd_phone"]  # 手机号输入框元素定位
    _email_locator = ["id", "memberAdd_mail"]  # 邮箱输入框元素定位
    _addr_locator = ["id", "memberEdit_address"]  # 地址输入框元素定位
    _save_member_locator = ["css selector", '.js_btn_save']  # 保存按钮元素定位
    _add_cancel_locator = ["css selector", '.js_btn_cancel']  # 取消按钮元素定位

    @allure.step("编辑成员信息")
    def edit_member(self, full_name, member_id, phone, email, **member_info):
        """
        编辑添加成员信息
        编辑的信息包括:
        必填参数: 姓名name,账号id,手机号phone，部门department(默认部门)
        选填参数: 别名alias，地址address,
        :param full_name: 必填参数姓名
        :param member_id: 必填参数账号
        :param phone: phone和email任选其一必填
        :param email: phone和email任选其一必填
        :param member_info:任一必填参数：手机号Phone 邮箱email, 其他选填参数  类型为字典
        :return: 当前页面对象，方便调用页面对象继续编辑成员信息
        """
        # 加入try,except容错处理
        try:
            log.logger.info(f"添加成员: {full_name}")
            self.input_text(*self._full_name_locator, full_name)  # 输入姓名
            self.input_text(*self._id_locator, member_id)  # 输入账号
            address = member_info.get("address")
            if phone or email:
                if phone:
                    self.input_text(*self._phone_locator, phone)  # 输入手机号
                else:
                    self.input_text(*self._email_locator, email)  # 输入邮箱
            elif address:
                self.input_text(*self._addr_locator, address)  # 输入地址
            else:
                log.logger.info(f"输入的选填参数为:{member_info}")
        except:
            raise Exception
        return self  # 链式调用

    @allure.step("点击保存按钮")
    def save_member(self):
        """
        保存添加成员
        :return: 页面跳转到通讯录页面，返回通讯录页面对象
        """
        try:
            self.click(*self._save_member_locator)  # 点击保存按钮
        except:
            raise Exception
        from page_objects.contacts_page import ContactsPage
        return ContactsPage(self.driver)  # 链式调用

    @allure.step("点击取消按钮")
    def add_cancel(self):
        """
        取消添加成员
        :param location_method: 取消按钮元素定位方式
        :param location_expression: 取消按钮元素定位表达式 ["css selector", '.js_btn_cancel']
        :return: 页面跳转到通讯录页面，返回通讯录页面对象
        """
        self.click(*self._add_cancel_locator)  # 点击添加成员页面cancel按钮
        from page_objects.contacts_page import ContactsPage  # 导入page_objects.contacts_page包，实现链式调用
        return ContactsPage(self.driver)  # 链式调用


# 测试代码
if __name__ == '__main__':
    from page_objects.home_page import HomePage

    params = {
        "email": "453323454@qq.com"
    }
    home_page = HomePage()  # 创建一个HomePage类实例
    home_page.open_browser("Chrome")  # 打开浏览器
    home_page.get_homepage_url()  # 打开homepage页面
    add_member_page = home_page.add_member_in_homepage()  # 点击添加成员
    add_member_page.edit_member("小白点", "NO010", 17345432234, email="453323454@qq.com")
    add_member_page.save_member()
