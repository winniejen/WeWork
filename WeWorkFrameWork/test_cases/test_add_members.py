#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

# @Description:添加成员测试用例
# @Author : jwy
# @Time : 2021/8/23 19:23
import os
import traceback

import allure
import pytest

from page_objects.common_operations import CommonOperations
from page_objects.contacts_page import ContactsPage
from page_objects.home_page import HomePage
from util.handle_excel import HandleExcel
from util.helper import projet_path
from util.handle_config_file import HandleConfigFile
from util.handle_yaml import read_yaml

# 测试数据
from util.log import log

add_members_test_data = read_yaml(os.path.join(projet_path(), "data/add_members_test_data.yaml"))['test_data']
# add_members_test_ids = read_yaml(os.path.join(projet_path(), "data/add_members_test_data.yaml"))
# 元素定位方式和定位值数据
add_member_locators = read_yaml(os.path.join(projet_path(), "data/add_member_locators.yaml"))
add_member_locator = add_member_locators['add_member_locator']
user_locator = add_member_locators['user_locator']
id_locator = add_member_locators['id_locator']
phone_locator = add_member_locators['phone_locator']
save_member_locator = add_member_locators['save_member_locator']
contacts_list_locator = add_member_locators['contacts_list_locator']

# 被测试的url
url_config = HandleConfigFile(os.path.join(projet_path(), "config.ini"))
home_page_url = url_config.get_option_value("TEST_URL", "home_page_url")

# excel关键字驱动测试数据
excel_file = HandleExcel(os.path.join(projet_path(), "data/wwork_contacts_testcases.xlsx"))
manage_member_sheet = excel_file.get_sheet_by_name("成员管理")
manage_member_testcases = excel_file.get_sheet_data(manage_member_sheet)

# excel列号与对应的列名
col_name_dict = {
    "cell_id": 0,
    "case_title": 3,
    "steps": 4,
    "is_run": 5,
    "action": 6,
    "ele_locator_method": 7,
    "ele_locator_expression": 8,
    "input_content": 9,
    "test_result": 13
}


# yaml关键字驱动测试数据
add_members_testcases = read_yaml(os.path.join(projet_path(), "data/add_members_testcases.yaml"))['test_case']


@allure.feature("添加成员")
class TestAddMembers:

    def setup_class(self):
        log.logger.info("---------开始测试添加成员功能--------")
        self.driver = None
        self.key_words = CommonOperations()

    def teardown_class(self):
        log.logger.info("---------添加成员功能测试结束----------")
        log.close()

    @allure.story("添加成员成功")
    @pytest.mark.parametrize("test_data", add_members_test_data)
    def test_add_member_success(self, test_data):
        allure.dynamic.title(test_data.get("case_name"))  # 在allure报告中显示标题
        # 获取测试数据，通过key获取获必填参数值，使用get()方法获取选填参数值
        # 通过key获取获取值，处理必填参数
        full_name = test_data['full_name']         # 姓名
        member_id = test_data['member_id']      # 账号
        phone = test_data.get("phone")           # 手机号
        email = test_data.get("email")        # 邮箱
        address = test_data.get("address")    # 地址
        try:
            home_page = HomePage()   # 创建一个HomePage类实例
            home_page.open_browser("Chrome")   # 打开浏览器
            home_page.get_homepage_url()   # 打开homepage页面
            add_member_page = home_page.add_member_in_homepage()  # 点击添加成员，跳转到添加成员页面
            add_member_page.edit_member(full_name, member_id, phone, email=email, address=address)   # 编辑成员信息
            contacts_page = add_member_page.save_member()    # 点击保存，跳转到通讯录页面
            # 判断添加成员成功，成功返回True,失败返回False
            add_member_result = contacts_page.assert_add_member_success(test_data['expect'])
            assert add_member_result == True
            log.logger.info("测试通过")
        except Exception as e:
            log.logger.error("测试失败")
            pytest.fail(f"添加成员失败")
            raise e

    @allure.story("通过关键字驱动添加成员,excel数据源")
    @pytest.mark.parametrize('test_data', manage_member_testcases)
    def test_add_member(self, test_data):
        cell_id = test_data[col_name_dict['cell_id']] + 1
        operate_step = test_data[col_name_dict['steps']]
        is_run = test_data[col_name_dict['is_run']]
        action = test_data[col_name_dict['action']]
        allure.dynamic.title(operate_step)
        params = []
        for i in range(col_name_dict['ele_locator_method'], col_name_dict['input_content']+1):
            if test_data[i] is not None:
                params.append(test_data[i])
        if is_run == "yes":
            func = getattr(self.key_words, action)
            try:
                log.logger.info(f"{operate_step}")
                func(*params)
                excel_file.write_cell(manage_member_sheet, "Pass", row=cell_id, col=col_name_dict['test_result'],
                                      style="green")
            except Exception as e:
                excel_file.write_cell(manage_member_sheet, "Fail", row=cell_id, col=col_name_dict['test_result'],
                                      style="red")
                log.logger.error(f"{operate_step}失败")
                pytest.fail("测试失败")
                raise e

    @allure.story("通过关键字驱动添加成员,yaml数据源")
    @pytest.mark.parametrize("test_cases", add_members_testcases)
    def test_add_members_03(self, test_cases):
        test_steps = test_cases["steps"]
        case_tile = test_cases['title']
        allure.dynamic.title(case_tile)
        for test_step in test_steps:
            step_name = test_step["name"]
            action = test_step["action"]
            element_locator = test_step["element_locator"]
            input_content = test_step["input_content"]
            with allure.step(step_name):
                try:
                    func = getattr(self.key_words, action)
                    if element_locator is None and input_content is None:
                        func()
                    elif element_locator is None and input_content is not None:
                        func(input_content)
                    elif element_locator is not None and input_content is None:
                        print("执行分支3")
                        func(*element_locator)
                    else:
                        func(*element_locator, input_content)
                except Exception as e:
                    pytest.fail(f"添加成员失败")
                    raise e


if __name__ == '__main__':
    pytest.main(['-vs', './test_add_members.py::TestAddMembers::test_add_members_03', '--alluredir',
                 '../results/temp', '--clean-alluredir'])
    os.system('allure generate ../results/temp -o ../results/reports --clean')
