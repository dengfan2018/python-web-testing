# -*- coding: utf-8 -*-
# @Time    : 2021/9/2 11:35
# @Author  : kanghe
# @Email   : 244783726@qq.com
# @File    : handle_ini.py

import os
import configparser

from common import handle_path as project


class HandleIni:
    """用来操作.ini格式的配置文件
    """

    def __init__(self, filename="pytest.ini", parent=project.base_dir):
        self.conf_path = parent.joinpath(filename)
        if not os.path.exists(self.conf_path):
            raise FileNotFoundError("配置文件不存在！")
        self.cf = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
        self.cf.read(self.conf_path, encoding="utf-8")

    def get_value(self, section, option, value_type="str"):
        """
        根据section和option读取配置文件具体的值"
        :param value_type: 
        :param section: 
        :param option: 
        :return: 
        """""
        if value_type == "str":
            return self.cf.get(section, option)
        elif value_type == "int":
            return self.cf.getint(section, option)
        elif value_type == "bool":
            return self.cf.getboolean(section, option)

    def get_section_value(self, section):
        """
        获取 section 下全部的值，返回字典形式"
        :param section: 
        :return: 
        """""
        return dict(self.cf.items(section))

    def get_option_all(self, section):
        """
        读取配置文件某个section下所有的option key
        :param section:
        :return:
        """
        return self.cf.options(section)

    def set_value(self, section, option, value):
        """设置配置文件中section下option的值"""
        self.cf.set(section, option, value)
        with open(self.conf_path, "w", encoding="utf8") as f:
            self.cf.write(f)

    def add_section(self, section):
        """在配置文件添加section"""
        self.cf.add_section(section)
        with open(self.conf_path, "w", encoding="utf8") as f:
            self.cf.write(f)


if __name__ == '__main__':
    cf = HandleIni()
    print(type(cf.get_value("setting", "timeout", value_type="int")))