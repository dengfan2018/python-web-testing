# -*- coding: utf-8 -*-
# @Time    : 2021/8/30 22:24
# @Author  : kanghe
# @Email   : 244783726@qq.com
# @File    : loc_login.py

from selenium.webdriver.common.by import By


class LocLogin:
    # 用户名输入框
    loc_username = (By.NAME, 'loginCall')
    # 密码输入框
    loc_passwd = (By.NAME, 'loginPassword')
    # 登陆按钮
    loc_login_button = (By.XPATH, '//button[contains(@class,"ok_btn_rd")]')


class LocLoginTesting:
    # 用户名输入框
    loc_username = (By.ID, 'nameOrEmail')
    # 密码输入框
    loc_passwd = (By.ID, 'loginPassword')
    # 登陆按钮
    loc_login_button = (By.ID, 'loginBtn')