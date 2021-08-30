# -*- coding: utf-8 -*-
# @Time    : 2021/8/30 22:21
# @Author  : kanghe
# @Email   : 244783726@qq.com
# @File    : basepage.py



from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
import os
import time

from Common.my_logger import logger
from Common.handle_path import screenshot_dir


class Basepage:

    def __init__(self,driver:WebDriver):
        self.driver = driver

    def wait_ele_visible(self, locator, page_action, timeout=20, poll_frequency=0.5):
        """
        :param locator:
        :param page_action:
        :param timeout:
        :param poll_frequency:
        :return:
        """
        logger.info("在 {} 行为，等待元素：{} 可见。".format(page_action,locator))
        try:
            start = time.time()
            WebDriverWait(self.driver, timeout,poll_frequency).until(EC.visibility_of_element_located(locator))
        except:
            # 输出到日志
            logger.exception("等待元素可见失败！")
            # 失败截取当前页面
            self.get_page_img(page_action)
            raise
        else:
            end = time.time()
            logger.info("等待耗时为：{}".format(end - start))

    def wait_page_contains_element(self, locator, page_action, timeout=20, poll_frequency=0.5):
        """
        :param locator:
        :param page_action:
        :param timeout:
        :param poll_frequency:
        :return:
        """
        logger.info("在 {} 行为，等待元素：{} 存在。".format(page_action,locator))
        try:
            start = time.time()
            WebDriverWait(self.driver, timeout,poll_frequency).until(EC.presence_of_element_located(locator))
        except:
            # 输出到日志
            logger.exception("等待元素存在失败！")
            # 失败截取当前页面
            self.get_page_img(page_action)
            raise
        else:
            end = time.time()
            logger.info("等待耗时为：{}".format(end - start))



    def get_element(self, locator, page_action,timeout=20, poll_frequency=0.5, wait_exist=False):
        """
        :param locator:
        :param page_action:
        :param timeout:
        :param poll_frequency:
        :param wait: 默认是等待元素可见。
        :return:
        """
        # 先等待元素可见或者存在
        if wait_exist is False:
            self.wait_page_contains_element(locator, page_action,timeout,poll_frequency)
        else:
            self.wait_ele_visible(locator, page_action,timeout,poll_frequency)

        logger.info("在 {} 行为，查找元素：{}".format(page_action,locator))
        try:
            ele = self.driver.find_element(*locator)
        except:
            # 输出到日志
            logger.exception("查找元素失败！")
            # 失败截取当前页面
            self.get_page_img(page_action)
            raise
        else:
            return ele

    def click_element(self,locator, page_action,timeout=20, poll_frequency=0.5):
        # 等待 - 查找
        ele = self.get_element(locator,page_action,timeout,poll_frequency)
        # 点击
        logger.info("在 {} 行为，点击元素：{}".format(page_action,locator))
        try:
            ele.click()
        except:
            logger.exception("点击元素失败！")
            self.get_page_img(page_action)
            raise

    def input_text(self,locator, page_action, value, timeout=20, poll_frequency=0.5):
        # 等待 - 查找
        ele = self.get_element(locator, page_action, timeout, poll_frequency)
        logger.info("在 {} 行为，给元素：{} 输入文本值：{}".format(page_action, locator, value))
        try:
            ele.clear()
            ele.send_keys(value)
        except:
            logger.exception("元素输入文本失败！")
            self.get_page_img(page_action)
            raise

    def get_text(self,locator, page_action, timeout=20, poll_frequency=0.5,wait_exist=False):
        """
        :param locator:
        :param page_action:
        :param timeout:
        :param poll_frequency:
        :return:
        """
        # 等待元素存在 - 查找
        ele = self.get_element(locator, page_action, timeout, poll_frequency,wait_exist=wait_exist)
        logger.info("在 {} 行为，获取元素 {} 的文本值。".format(page_action, locator))
        try:
            txt = ele.text
        except:
            logger.exception("获取元素文本失败！")
            self.get_page_img(page_action)
            raise
        else:
            logger.info("文本值为：{}".format(txt))
            return txt

    def get_attribute(self,locator, page_action, attr, timeout=20, poll_frequency=0.5, wait_exist=False):
        # 等待元素存在 - 查找
        ele = self.get_element(locator, page_action, timeout, poll_frequency, wait_exist=wait_exist)
        logger.info("在 {} 行为，获取元素 {} 的 {} 属性值。".format(page_action, locator,attr))
        try:
            value = ele.get_attribute(attr)
        except:
            logger.exception("获取元素文本失败！")
            self.get_page_img(page_action)
            raise
        else:
            logger.info("属性值为：{}".format(value))
            return value

    def switch_window(self,name="new"):
        # 等待一下
        time.sleep(1)
        # 获取所有的句柄
        wins = self.driver.window_handles
        if name == "new":
            driver.switch_to.window(wins[-1])

    # js的值来修改value值。 -- 固定流程，你都是可以封装。
    # driver.find_element()来找到元素。传到js里面，arguments[0].value=new_value

    def back_last_page(self):
        logger.info("回退到上一页")
        self.driver.back()
        return self

    def refresh_page(self):
        logger.info("刷新当前页面")
        self.driver.refresh()
        return self

    def get_page_img(self,page_action):
        # 命令规范: {XX页面_XX操作}_截图时间.png
        cur_time =  time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())
        file_path = os.path.join(screenshot_dir,"{}_{}.png".format(page_action,cur_time))
        self.driver.save_screenshot(file_path)
        logger.info("截图保存在：{}".format(file_path))


if __name__ == '__main__':
    from selenium import webdriver
    from time import sleep
    driver = webdriver.Chrome()
    base = Basepage(driver)
    driver.get("http://www.baidu.com")
    # 等待输入框可见
    loc = ("id","kw")
    loc_button = ("id", "su")

    base.input_text(loc,"百度首页_输入搜索内容","selenium webdriver")
    base.click_element(loc_button,"百度首页_点击搜索按钮")

    sleep(7)
    driver.quit()
