# -*- coding: utf-8 -*-
# @Time    : 2021/9/1 20:38
# @Author  : kanghe
# @Email   : 244783726@qq.com
# @File    : handle_path.py

from pathlib import Path


base_dir = Path(__file__).resolve().parent.parent


# 测试报告的路径
reports_dir_allure_temp = str(base_dir.joinpath("output", "allure"))
reports_dir_allure_html = str(base_dir.joinpath("output", "allure-html"))

# 截图存放路径
image_dir = str(base_dir.joinpath("output", "images"))

# 日志的路径
logs_dir = base_dir.joinpath("logs")

# chromedriver 路径
chrome_driver = str(base_dir.joinpath("utils", "chromedriver.exe"))
