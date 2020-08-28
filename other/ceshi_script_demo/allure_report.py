#!/usr/bin/python3
# -*- coding:utf-8 -*-

import demo, allure


@allure.MASTER_HELPER.step('字符串相加：{0}，{1}')
def str_add(str1, str2):
    print('hello')
    if not isinstance(str1, str):
        return '%s is not a string' % str1
    if not isinstance(str2, str):
        return '%s is not a string' % str2
    return str1 + str2


'''
severity：优先级(blocker, critical, normal, minor, trivial)
feature：功能块，feature功能分块时比story大,即同时存在feature和story时,feature为父节点
story：功能块，具有相同feature或story的用例将规整到相同模块下,执行时可用于筛选
issue：问题表识，关联标识已有的问题，可为一个url链接地址
testcase：用例标识，关联标识用例，可为一个url链接地址
parametrize：(用例参数, 用例参数的参数化数据, 对应用例参数化数据的用例名)
'''
@allure.MASTER_HELPER.severity('critical')
@allure.MASTER_HELPER.feature('测试模块_demo1')
@allure.MASTER_HELPER.story('测试模块_demo2')
@allure.MASTER_HELPER.issue('BUG号：123')
@allure.MASTER_HELPER.testcase('用例名：测试字符串相等')
@demo.mark.parametrize('para_one, para_two',
                       [("hello world", "hello world"), ('4', '4'), ("中文", "中文")],
                       ids=["test ASCII string", "test digital string", "test unicode string"]
                       )
def test_case_example(para_one, para_two):
    ''' 用例描述：测试字符串相等
    :param para_one: 参数1
    :param para_two: 参数2
    :return:
    '''
    # 获取参数
    paras = vars()
    # 报告中的环境参数，可用于必要环境参数的说明，相同的参数以后者为准
    allure.MASTER_HELPER.environment(host='127.0.0.1', test_vars=paras)
    # 关联的资料信息, 可在报告中记录保存必要的相关信息
    allure.MASTER_HELPER.attach('用例参数', '{0}'.format(paras))
    # 调用测试函数
    res = str_add(para_one, para_two)
    # 对必要的测试中间结果数据做备份
    allure.MASTER_HELPER.attach('str_add返回结果', '{0}'.format(res))
    # 测试步骤，对必要的测试过程加以说明
    with allure.MASTER_HELPER.step("测试步骤2，结果校验 {0} == {1}".format(res, para_one+para_two)):
        assert res == para_one + para_two, res


if __name__ == '__main__':
    # 执行，指定执行测试模块_demo1, 测试模块_demo2两个模块，同时指定执行的用例优先级为critical,blocker
    demo.main(['--allure_stories=测试模块_demo1, 测试模块_demo2', '--allure_severities=critical, blocker'])

# 执行命令：demo allure_report.py --alluredir report
