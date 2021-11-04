#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

# @Description:封装基础类BasePage，包含driver的初始化，元素定位,显示等待，获取元素的属性，页面截图等的二次封装等。
# @Author : jwy
# @Time : 2021/8/23 17:26
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from util.log import log


class CommonOperations:
    """
    封装页面元素操作的基础类和对driver的初始化
    """

    def __init__(self, base_driver=None):
        """
        创建构造函数，初始化driver
        :param base_driver: 第一次调用时，base_driver为None，通过调用open_browser获取响应的driver对象
                            在继承的子类中，如果已经获取到driver，那么则复用传入的driver
        """
        if base_driver is None:
            self.driver: WebDriver = None
        else:
            self.driver = base_driver

    def open_browser(self, browser):
        """
        打开浏览器
        :param browser: 浏览器名称
        :return: 浏览器driver
        """
        try:
            if browser == "Chrome":
                chrome_option = Options()  # 创建chrome浏览器的一个Options实例对象
                # 设置远程web服务调试地址为本机端口为9222，在终端开启这个调试端口来实现浏览器复用
                chrome_option.debugger_address = '127.0.0.1:9222'
                self.driver = webdriver.Chrome(options=chrome_option)
                return self.driver
            elif browser == "Firefox":
                self.driver = webdriver.Firefox()
            elif browser == "Ie":
                self.driver = webdriver.Ie()
            else:
                self.driver = webdriver.Edge()
        except Exception as e:
            raise e

    def get_url(self, url):
        """
        打开网址
        :param url: 网站地址
        """
        # 访问某一个网址,最大化窗口
        try:
            self.driver.get(url)
            self.driver.implicitly_wait(5)  # 隐式等待，全局等待5s
            self.driver.maximize_window()
        except Exception as e:
            log.logger.error(f"打开网页{url}失败！")
            raise e

    def get_element(self, location_method, location_expression):
        """
        获取单个页面元素对象
        :param location_method: 定位方式
        :param location_expression: 定位表达式
        :return: 页面元素对象
        """
        # 加入容错处理
        try:
            return self.driver.find_element(location_method, location_expression)
        except Exception as e:
            log.logger.error(f"页面元素({location_method},{location_expression})未找到！")
            raise e

    def get_elements(self, location_method, location_expression):
        """
        获取多个相同页面元素对象，以list返回
        :param location_method: 定位方式
        :param location_expression: 定位表达式
        :return: 这一类元素对象的列表
        """
        # 加入try,except捕获异常，增加容错处理
        try:
            return self.driver.find_elements(location_method, location_expression)
        except Exception as e:
            log.logger.error(f"页面元素({location_method},{location_expression})未找到")
            raise e

    def input_text(self, location_method, location_expression, input_content):
        """
        在页面输入框中输入数据
        :param location_method: 定位方式
        :param location_expression: 定位表达式
        :param input_content: 输入的内容
        """
        # 加入try,except捕获异常，增加容错处理
        try:
            self.get_element(location_method, location_expression).send_keys(input_content)
        except Exception as e:
            log.logger.error(f"在页面元素({location_method},{location_expression})输入{input_content}失败！")
            raise e

    def click(self, location_method, location_expression):
        """
        单击页面元素
        :param location_method: 定位方式
        :param location_expression: 定位表达式
        :return:
        """
        # 加入try,except捕获异常，增加容错处理
        try:
            self.get_element(location_method, location_expression).click()
        except Exception as e:
            log.logger.error(f"页面元素({location_method},{location_expression})不可点击！")
            raise e

    def wait_time(self, time):
        """
        强制等待
        :param time: 等待时间
        :return:
        """
        sleep(time)

    def wait_element_located(self, locator, timeout=20, frequency=0.5):
        """
        显示等待页面元素出现在dom中，但并不一定可见，存在则返回该元素的对象
        :param locator: 元素定位方式和定位表达式，可以是元祖或列表
        :param timeout: 等待时间，默认20s
        :param frequency: 查找频率 默认0.5s
        :return: 页面元素对象
        """
        # 加入try,except捕获异常，增加容错处理
        try:
            WebDriverWait(self.driver, timeout, frequency).until(
                EC.presence_of_element_located(locator))
        except:
            log.logger.error(f"等待页面元素{locator}加载超时！")
            raise Exception

    def wait_element_visible(self, locator, timeout=20, frequency=0.5):
        """
        显示等待页面元素出现在dom中，并且可见，存在则返回该元素的对象
        :param locator: 元素定位方式和定位表达式，可以是元祖或列表
        :param timeout: 等待时间，默认20s
        :param frequency: 查找频率 默认0.5s
        :return: 页面元素对象
        """
        # 加入try,except捕获异常，增加容错处理
        try:
            WebDriverWait(self.driver, timeout, frequency).until(
                EC.visibility_of_element_located(locator))
        except:
            log.logger.error(f"等待页面元素{locator}可见超时！")
            raise Exception

    def wait_element_clickable(self, locator, timeout=20, frequency=0.5):
        """
        显示等待页面元素出现在dom中，并且可点击
        :param locator: 元素定位方式和定位表达式，可以是元祖或列表
        :param timeout: 等待时间，默认20s
        :param frequency: 查找频率 默认0.5s
        :return: 页面元素对象
        """
        # 加入try,except捕获异常，增加容错处理
        try:
            WebDriverWait(self.driver, timeout, frequency).until(
                EC.element_to_be_clickable(locator))
        except:
            log.logger.error(f"等待页面元素{locator}可点击超时！")
            raise Exception

    def save_screenshot(self, file_name):
        """
        保存页面截图
        :param file_name: 截图文件
        :return:
        """
        self.driver.save_screenshot(file_name)

    def get_text(self, location_method, location_expression):
        """
        获取页面元素text属性值，作为测试用例的断言信息
        :param location_method: 元素定位方式
        :param location_expression: 元素定位值
        :return:
        """
        # 加入try,except捕获异常，增加容错处理
        try:
            self.get_element(location_method, location_expression).text()
        except:
            log.logger.error(f"获取页面元素({location_method},{location_expression})text属性失败！")
            raise Exception

    def assert_text(self, text):
        """
        断言页面源码中是否存在某关键字或关键字符串
        :param text:
        :return:
        """
        try:
            assert text in self.driver.page_source
        except AssertionError as e:
            raise AssertionError(e)
        except Exception as e:
            raise e


# 调用BasePage类中方法，测试各方法功能是否正确
if __name__ == '__main__':
    pass
    # key_words = CommonOperations()
    # driver = base_page.driver  # 创建BasePage类对象，初始化chrome浏览器
    # base_page.open_browser("Chrome")
    # print(driver)
    # base_page.get_url("http://www.baidu.com")  # 打开百度
    # base_page.input_text("id", "kw", "自动化测试")  # 在输入框中搜索"自动化测试"
    # base_page.click("id", "su")  # 点击"百度一下"
    # base_page.click("css selector", r"#\33 001 .wbrjf67>a")  # 在返回结果中点击第一个选项
