# -*- coding: utf-8 -*-
# @Time    : 2021/9/1 20:33
# @Author  : kanghe
# @Email   : 244783726@qq.com
# @File    : conftest.py
import os
import warnings

import pytest
import allure
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

from common.handle_ini import HandleIni
from common.handle_path import chrome_driver, image_dir

from polocator.loc_login import LocLogin


web_driver: WebDriver = None

cf = HandleIni()
implicitly_wait_time = cf.get_value("setting", "implicitly_wait_time", value_type="int")


@pytest.fixture(scope="class")
def driver():

    option = webdriver.ChromeOptions()

    # 不显示 Chrome正受到自动测试软件控制 、 开发者提示
    option.add_experimental_option("excludeSwitches", ['enable-automation', 'load-extension'])

    # # 专门应对无头浏览器中不能最大化屏幕的方案
    # option.add_argument('--headless')
    # option.add_argument("--window-size=1920x1080")

    global web_driver
    driver = webdriver.Chrome(options=option, executable_path=chrome_driver)

    # 设置隐性等待时间，全局设置一次即可
    driver.implicitly_wait(implicitly_wait_time)

    # 最大化浏览器
    driver.maximize_window()

    web_driver = driver
    yield driver

    driver.quit()


@pytest.fixture(scope="class")
def login_eo(driver_selenium_grid):
    project_url = cf.get_value("eolinker", "url")
    web_driver.get(project_url)
    # web_driver.find_element(*LocLogin.loc_username).send_keys(cf.get_value("login", "user"))
    # web_driver.find_element(*LocLogin.loc_passwd).send_keys(cf.get_value("login", "password"))
    # web_driver.find_element(*LocLogin.loc_login_button).click()
    web_driver.save_screenshot(f"{image_dir}b.png")
    yield web_driver


@pytest.fixture(scope="class")
def login_testing(driver_selenium_grid):
    project_url = cf.get_value("testingpai", "url")
    web_driver.get(project_url)
    # web_driver.find_element(*LocLogin.loc_username).send_keys(cf.get_value("login", "user"))
    # web_driver.find_element(*LocLogin.loc_passwd).send_keys(cf.get_value("login", "password"))
    # web_driver.find_element(*LocLogin.loc_login_button).click()
    web_driver.save_screenshot(f"{image_dir}a.png")
    yield web_driver


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    断言失败的用例自动截图(执行失败和断言失败)
    :param item:
    :param call:
    :return:
    """
    outcome = yield
    rep = outcome.get_result()
    # print(rep)
    if rep.when == "call" and rep.failed:

        # mode = "a" if os.path.exists("failures") else "w"
        # with open("failures", mode) as f:
        #     # let's also access a fixture for the fun of it
        #     if "tmpdir" in item.fixturenames:
        #         extra = " (%s)" % item.funcargs["tmpdir"]
        #     else:
        #         extra = ""
        #     f.write(rep.nodeid + extra + "\n")

        if hasattr(web_driver, "get_screenshot_as_png"):
            with allure.step("失败截图"):
                allure.attach(web_driver.get_screenshot_as_png(), "失败截图", allure.attachment_type.PNG)


@pytest.fixture(scope="class")
def driver_selenium_grid():
    remote_url = cf.get_value("setting", "selenium_hub")

    warnings.simplefilter("ignore", ResourceWarning)
    ds = {'platform': 'ANY',
          'browserName': "chrome",
          'version': '',
          'javascriptEnabled': True
          }

    global web_driver
    driver = webdriver.Remote(remote_url, desired_capabilities=ds)

    # 设置隐性等待时间，全局设置一次即可
    driver.implicitly_wait(10)

    web_driver = driver
    yield driver

    driver.quit()
