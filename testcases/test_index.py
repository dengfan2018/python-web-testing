# -*- coding: utf-8 -*-
# @Time    : 2021/8/30 22:25
# @Author  : kanghe
# @Email   : 244783726@qq.com
# @File    : test_index.py

import pytest


# @pytest.mark.usefixtures("login")
class TestLogin:

    # 逆向场景 - 登陆失败 - 数据格式无效
    # @pytest.mark.parametrize("case", )
    def test_login_failed_invalid_data(self, login_eo):
        ...
