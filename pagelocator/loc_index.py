# -*- coding: utf-8 -*-
# @Time    : 2021/8/30 22:24
# @Author  : kanghe
# @Email   : 244783726@qq.com
# @File    : loc_index.py

from selenium.webdriver.common.by import By

class LoginPageLocs:
    # 用户名输入框
    username_loc = (By.XPATH, '//input[@name="phone"]')
    # 密码输入框
    passwd_loc = (By.XPATH, '//input[@name="password"]')
    # 登陆按钮
    login_button_loc = (By.TAG_NAME, 'button')
    # 登陆区域的提示框
    error_tips_from_login_area = (By.XPATH, '//div[@class="form-error-info"]')