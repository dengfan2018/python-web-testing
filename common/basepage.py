# -*- coding: utf-8 -*-
# @Time    : 2021/8/30 22:21
# @Author  : kanghe
# @Email   : 244783726@qq.com
# @File    : basepage.py

import os
import time
from datetime import date

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException

from common.handle_path import image_dir
from common.handle_log import log


class BasePage:

    def __init__(self, driver: WebDriver):
        self.driver = driver

    @staticmethod
    def get_time(pattern="%Y-%m-%d %H_%M_%S"):
        """
        日期时间相关方法之一
        :param pattern: 日期时间格式化输出， 默认为 %Y-%m-%d %H_%M_%S
        :return: 返回格式化输出的时间
        """
        return time.strftime(pattern, time.localtime(time.time()))

    @staticmethod
    def get_date():
        """
        日期时间相关方法之一
        :return: 返回当前日期，格式为 %Y-%m-%d
        """
        return str(date.today())

    def find_element_wait(self, locator, index: int = 0, timeout=15):
        """
        driver.find_element 方法封装，兼容多种情况。如 locator 定位到多个元素，通过 index 来选择。
        :param locator:
        :param index: locator 定位索引，从0开始，默认为 0
        :param timeout:
        :return:
        """

        try:
            elements = WebDriverWait(self.driver, timeout).until(lambda ele: self.driver.find_elements(*locator))
            if elements:
                return elements[index]
            else:
                raise NoSuchElementException
        except Exception as e:
            log.erro(f"查找{locator}元素时间超时\n {e}")
            self.save_img("元素查找失败")

    def click(self, locator, index=0):
        try:
            return self.find_element_wait(locator, index).click()
        except Exception as e:
            log.error('点击元素{}失败！\n {}'.format(locator, e))
            self.save_img("点击失败")

    def send_text(self, locator, text, index=0):
        try:
            self.find_element_wait(locator, index).send_keys(text)
        except Exception as e:
            log.error('{}元素输入{}失败！\n {}'.format(locator, text, e))
            self.save_img("输入失败")

    # 获取元素文本内容
    def get_text(self, locator, index=0):
        ele = self.find_element_wait(locator, index)
        try:
            return ele.text
        except Exception as e:
            log.info('获取元素{}的文本内容失败！\n {}'.format(locator, e))
            self.save_img("获取文本失败")

    def switch_new_window(self):
        """
        切换到新开的窗口
        :return:
        """
        self.window_handles()
        self.switch_to_window(self.window_handles()[-1])

    # 切换到iframe页面
    def switch_iframe(self, locator):
        try:
            WebDriverWait(self.driver, 25).until(ec.frame_to_be_available_and_switch_to_it(locator))
            return self
        except Exception as e:
            log.info('{} iframe切换失败！'.format(locator))
            raise e

    # 切换到父级iframe页面
    def switch_iframe_parent(self):
        try:
            return self.driver.switch_to.parent_frame()
        except Exception as e:
            log.info("切换到父级iframe失败")
            raise e

    # 鼠标聚焦在元素上
    def move_mouse_to_element(self, locator, many=0):
        ele = self.find_element_wait(locator, many)
        try:
            webdriver.ActionChains(self.driver).move_to_element(ele).perform()
            return self
        except Exception as e:
            log.info("鼠标在元素{}聚焦失败！".format(ele))
            raise e

    # 执行js脚本
    def execute_js(self, js):
        self.driver.execute_script(js)

    # 针对element执行js脚本
    def execute_js_ele(self, locator, js, index=0):
        ele = self.find_element_wait(locator, index)
        self.driver.execute_script(f"arguments[0].{js}", ele)

    # 滚动页面：移动页面至元素可见
    def execute_js_view(self, locator):
        ele = self.wait_ele_presence(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", ele)

    def execute_js_click(self, locator, index=0):
        log.info(f"使用js点击{locator}")
        element = self.find_element_wait(locator, index)
        self.driver.execute_script("arguments[0].click();", element)

    @staticmethod
    def sleep(second):
        time.sleep(second)

    # 保留截图
    def save_img(self, name):
        if not os.path.exists(image_dir):
            log.info('{} not exists, create it'.format(image_dir))
            os.makedirs(image_dir)
        file_name = os.path.join(image_dir, name + "_" + self.get_time() + ".png")
        self.driver.get_screenshot_as_file(file_name)
        log.info("截取网页成功。文件名称为：{}".format(file_name))
        return file_name

    # 获取元素属性
    def get_element_attr(self, locator, attr, index=0):
        ele = self.find_element_wait(locator, index)
        try:
            return ele.get_attribute(attr)
        except Exception as e:
            log.info('获取元素{}的属性失败！'.format(locator))
            raise e

    # 判断页面上是否存在alert
    def wait_alert(self, times=20, poll_frequency=0.5):
        try:
            WebDriverWait(self.driver, times, poll_frequency).until(ec.alert_is_present())
        except Exception as e:
            message = 'Alert Element: cannot be found in {0} seconds.'.format(times)
            log.info(message)
            raise e

    # 切换到alert弹窗
    def switch_alert(self):
        try:
            WebDriverWait(self.driver, 25).until(ec.alert_is_present())
            return self.driver.switch_to.alert
        except Exception as e:
            log.info('切换到alert失败')
            raise e

    # 切换到主页面
    def switch_to_default_content(self):
        try:
            self.driver.switch_to.default_content()
        except Exception as e:
            log.info("切换到主页面失败")
            raise e

    # 切换浏览器窗口
    def switch_to_window(self, window):
        try:
            self.driver.switch_to.window(window)
        except Exception as e:
            log.info("切换窗口失败")
            raise e

    # 获取浏览器所有窗口
    def window_handles(self):
        return self.driver.window_handles

    # 获取当前窗口
    def current_window_handle(self):
        return self.driver.current_window_handle

    def wait_ele_visible(self, locator, timeout=15):
        """
        等待元素可见

        :param locator:定位的元素,形式为元组格式的，如(By.XPATH,'')
        :param timeout:最长等待时间

        :return: 返回一个 elements 对象，可以直接进行 click 等操作
        """
        ele = None
        try:
            ele = WebDriverWait(self.driver, timeout).until(ec.visibility_of_element_located(locator))
        except Exception as e:
            log.error('等待元素{}可见失败！{}'.format(locator, e))
            self.save_img(f"等待元素可见失败")
        return ele

    def wait_ele_presence(self, locator, timeout=15):
        """
        等待元素存在
        """
        try:
            ele = WebDriverWait(self.driver, timeout).until(ec.presence_of_element_located(locator))
            return ele
        except Exception as e:
            log.info('等待元素{}存在失败！'.format(locator))
            self.save_img(f"等待存在失败")
            raise e

    def wait_page_contains_element(self, locator, page_action, timeout=20, poll_frequency=0.5):
        """
        :param locator:
        :param page_action:
        :param timeout:
        :param poll_frequency:
        :return:
        """
        log.info("在 {} 行为，等待元素：{} 存在。".format(page_action, locator))
        try:
            start = time.time()
            WebDriverWait(self.driver, timeout, poll_frequency).until(ec.presence_of_element_located(locator))
        except:
            # 输出到日志
            log.exception("等待元素存在失败！")
            # 失败截取当前页面
            self.save_img(page_action)
            raise
        else:
            end = time.time()
            log.info("等待耗时为：{}".format(end - start))


if __name__ == '__main__':
    from selenium import webdriver
    from time import sleep
