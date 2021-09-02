# -*- coding: utf-8 -*-
# @Time    : 2021/9/2 15:32
# @Author  : kanghe
# @Email   : 244783726@qq.com
# @File    : main.py

import os


if __name__ == '__main__':
    os.system(f"pytest -s -v ")
    # os.system(f"pytest -s -v --alluredir={reports_dir_allure_temp} --clean-alluredir")
    # os.system(f"allure generate -c -o {reports_dir_allure_html} {reports_dir_allure_temp}")
