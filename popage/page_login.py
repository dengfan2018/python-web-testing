# -*- coding: utf-8 -*-
# @Time    : 2021/8/30 22:25
# @Author  : kanghe
# @Email   : 244783726@qq.com
# @File    : page_login.py

from common.basepage import BasePage
from polocator.loc_login import LocLogin


class LoginPage(BasePage):

    def login(self, user, passwd):
        self.send_text(LocLogin.loc_username, user)
        self.send_text(LocLogin.loc_passwd, passwd)
        self.click(LocLogin.loc_login_button, "登陆页面_点击登陆按钮")
