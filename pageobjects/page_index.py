# -*- coding: utf-8 -*-
# @Time    : 2021/8/30 22:25
# @Author  : kanghe
# @Email   : 244783726@qq.com
# @File    : page_index.py

from PageLocators.login_page_locs import LoginPageLocs as loc
from Common.basepage import Basepage



class LoginPage(Basepage):

    def login(self,user,passwd):
        self.input_text(loc.username_loc,"登陆页面_输入用户名",user)
        self.input_text(loc.passwd_loc,"登陆页面_输入密码",passwd)
        self.click_element(loc.login_button_loc,"登陆页面_点击登陆按钮")

    def get_error_msg_from_login_area(self):
        return self.get_text(loc.error_tips_from_login_area,"登陆页面_获取登陆区错误提示信息")
