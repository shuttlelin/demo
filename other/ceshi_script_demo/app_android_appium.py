#!/usr/bin/python3
# -*- coding:utf-8 -*-

from appium import webdriver
from time import sleep


desired_caps = {}  # 定义初始化的属性信息
desired_caps['platformName'] = 'Android'  # 设备系统
desired_caps['platformVersion'] = '4.4.4'  # 设备系统版本
desired_caps['deviceName'] = 'Android Emulator'  # 设备名称
desired_caps['appPackage'] = 'com.android.calculator2'  # 包名，获得包名的方式有很多
desired_caps['appActivity'] = '.Calculator'  # Activity，获得的方式也很多
desired_caps['unicodeKeyboard'] = True  # 使用unicodeKeyboard的编码方式来发送字符串
desired_caps['resetKeyboard'] = True  # 将键盘给隐藏起来

driver = webdriver.Remote('http://', desired_caps)  # 启动服务器地址，后面跟的是手机信息
driver.find_element_by_name('1').click()  # 点击计算器中的1
driver.find_element_by_name('5').click()
driver.find_element_by_name('9').click()
driver.find_element_by_name('delete').click()
driver.find_element_by_name('9').click()
driver.find_element_by_name('5').click()
driver.find_element_by_name('+').click()
driver.find_element_by_name('6').click()
driver.find_element_by_name('=').click()
sleep(10)
driver.quit()
