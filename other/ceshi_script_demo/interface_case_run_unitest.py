#!/usr/bin/python3
# -*- coding:utf-8 -*-

import unittest
from other.ceshi_script_demo.interface_case_one_unitest import Case_One
from other.ceshi_script_demo.case_two_unitest import Case_Two


'''
unittest是python自带的单元测试框架，有时候又被称为”PyUnit”，是python版本的JUint实现。
在学习使用unittest库之前，我们需要了解一下unittest库的一些重要概念:
    test fixture: 代表了用例执行前的准备工作和用例执行之后的清理工作。比如在用例执行前创建临时文件和文件夹，又或者启动1个server进程等；
    test case: 测试用例，这个相信大家都不陌生。是测试的最小单位，一般检查一组输入的响应(输出)是否符合预期。unittest模块提供了TestCase类来帮助我们创建测试用例；
    test suite: 经常被翻译成”测试套件”，也有人称为”测试套”，是测试用例或测试套件的集合，一般用来把需要一起执行的用例组合到一起;
    test runner: 用来执行测试用例并输出测试结果的组件。可以是图形界面或命令行界面;
总之
    test fixture的功能可以理解成是初始化和清理测试数据及环境
    test case是测试用例
    test suite是用例集合
    test runner的作用是运行用例并返回结果
'''

suite = unittest.TestSuite()
suite.addTest(Case_One('test_case_one'))
suite.addTest(Case_Two('test_case_two'))
unittest.TextTestRunner().run(suite)
# 下面2行 等同于 上面1行
# st = open('./report.html', 'wb') # 输出的文件路径
# HTMLTestRunnerCN.HTMLTestRunner(stream=st, title='接口自动化项目', teste='sldeng').run(suite) # 生成报告
