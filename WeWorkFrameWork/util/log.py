#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

# @Description:输出日志到控制台和文件中
# @Author : jwy
# @Time : 2021/8/24 16:23

import logging
import time

# 设置log输出的地址和日志的名称
from util.helper import projet_path

log_path = projet_path() + "/logs/"  # 设置日志输出地址
log_file_name = log_path + time.strftime("%Y_%m_%d_") + "log.log"  # 设置日志保存的文件名称


class Log:
    def __init__(self, name=None, set_level="DEBUG"):
        self.logger = logging.getLogger(name)  # 创建日志器对象
        self.logger.setLevel(level=set_level)  # 默认warning  logger和handler两个地方设置，取优先级高的那个
        self.logger = self.get_log()  # 设置日志器对象

    def console_handle(self, set_level="DEBUG"):
        console_handler = logging.StreamHandler()  # 创建控制台处理器
        console_handler.setLevel(level=set_level)  # 控制台日志输出等级
        console_handler.setFormatter(self.get_fomatter()[0])  # 设置控制台处理器日志格式
        return console_handler

    def file_handle(self, set_level="INFO"):
        file_handler = logging.FileHandler(log_file_name, mode="a", encoding="utf-8")
        file_handler.setLevel(level=set_level)  # 设置文件处理器的日志输出等级
        file_handler.setFormatter(self.get_fomatter()[1])  # 设置文件处理器日志格式
        return file_handler

    def get_fomatter(self):
        console_fmt = "%(name)s %(levelname)s %(message)s"
        file_fmt = "%(asctime)s %(filename)s %(funcName)s line:%(lineno)d [%(levelname)s] %(message)s"
        fmt1 = logging.Formatter(fmt=console_fmt)  # 设置控制台输出的日志格式
        fmt2 = logging.Formatter(fmt=file_fmt)  # 设置文件输出的日志格式
        return fmt1, fmt2

    def get_log(self):
        self.logger.addHandler(self.console_handle())  # 将控制台处理器添加到日志器
        self.logger.addHandler(self.file_handle())  # 将文件处理器添加到日志器
        return self.logger

    def close(self):
        self.logger.removeHandler(self.console_handle())  # 将控制台处理器从日志器移除
        self.logger.removeHandler(self.file_handle())  # 将文件处理器从日志器移除
        self.file_handle().close()


log = Log()  # 单例模式

# 测试代码
if __name__ == '__main__':
    log = Log()
    log.logger.debug("这是一debug条日志")
    log.logger.critical("这是一条critical日志")
    log.logger.error("这是一条error级别的日志")
