#!/usr/bin/python3
# -*- coding:utf-8 -*-

import json, smtplib, requests


'''
scope
    function：每个test都运行，默认是function的scope
    class：每个class的所有test只运行一次
    module：每个module的所有test只运行一次
    session：每个session只运行一次
调用fixture的三种方式
    在测试用例中直接调用它
    用fixture decorator调用fixture
        第一种是每个函数前声明
        第二种是封装在类里，类里的每个成员函数声明
        第三种是封装在类里在前声明
    用autos调用fixture 【默认设置为False】
        当默认为False，就可以选择用上面两种方式来试用fixture
        当设置为True时，在一个session内的所有的test都会自动调用这个fixture
assert 0：强制用例失败，这样可以看到每次fixture的参数值
生成xml格式的测试报告：demo_pytest test_pytest.py --junit-xml=report.xml
'''


# 基本
def reverse(string):
    return string[::-1]


def test_reverse():
    str = 'good'
    assert reverse(str) == 'doog'
    assert reverse('itest') == 'tseti'

# assert
# def test_zero_division():
#     with demo_pytest.raises(ZeroDivisionError):
#         1/0
#     with demo_pytest.raises(RuntimeError) as excinfo:
#         def f():
#             f()
#         f()
#     assert 'maximum recursoin' in str(excinfo.value)

# fixture
# class TestUserPassword(object):
#     @demo_pytest.fixture
#     def users(self):
#         return json.loads(open('user_data.json', 'r').read())
#     def test_user_password(self, users):
#         for user in users:
#             pwd = user['passwd']
#             assert len(pwd) >= 6
#             msg = 'user %s has a weak password' % user['name']
#             assert pwd != 'password', msg
#             assert pwd != 'password123', msg
# 数据清理
# @demo_pytest.fixture(scope='module')
# def smtp():
#     smtp = smtplib.SMTP('smtp.gmail.com', 587, timeout=5)
#     yield smtp
#     print('teardown smtp')
#     smtp.close()

# 参数化的Fixture
# @demo_pytest.fixture(scope="module", params=["smtp.gmail.com", 'mail.python.org'])
# def smtp(request):
#     smtp = smtplib.SMTP(request.param, 587, timeout=5)
#     yield smtp
#     print('finalizing %s' % smtp)
#     smtp.close()
#
# users = json.loads(open('user_data.json', 'r').read())
# class TestPasswordWithParam(object):
#     @demo_pytest.fixture(params=users)
#     def user(self, request):
#         return request.param
#     def test_user_password(self, user):
#         pwd = user['passwd']
#         assert len(pwd) >= 6
#         msg = 'user %s has a weak password' % user['name']
#         assert pwd != 'password', msg
#         assert pwd != 'password123', msg

# Parametrize Fixture
# @demo_pytest.mark.parametrize('test_input, expected', [('3+5', 8), ('2+4', 6), ('6*9', 42)])
# def test_eval(test_input, expected):
#     assert eval(test_input) == expected

# 简单的接口测试
# class TestV2exApi(object):
#     domain = 'https://www.v2ex.com/'
#     def test_node(self):
#         path = 'api/nodes/show.json?name=python'
#         url = self.domain + path
#         res = requests.get(url).json()
#         assert res['id'] == 90
#         assert res['name'] == 'python'

# 使用fixture参数化接口入参
# class TestV2exWithParam(object):
#     domain = 'https://www.v2ex.com/'
#     @demo_pytest.fixture(params=['python', 'java', 'go', 'nodejs'])
#     def lang(self, request):
#         return request.param
#     def test_node(self, lang):
#         path = 'api/nodes/show.json?name=%s' % lang
#         url = self.domain + path
#         res = requests.get(url).json()
#         assert res['name'] == lang
#         assert 0 # 使用该行，强制用例失败，这样可以看到每次fixture的参数值

# 使用fixture参数化测试预期结果
# class TestV2exApiWithExpectation(object):
#     domain = 'https://www.v2ex.com/'
#     @demo_pytest.mark.parametrize('name, node_id', [('python', 90), ('java', 63), ('go', 375), ('nodejs', 436)])
#     def test_node(self, name, node_id):
#         path = 'api/nodes/show.json?name=%s' % name
#         url = self.domain + path
#         res = requests.get(url).json()
#         assert res['name'] == name
#         assert res['id'] == node_id
#         assert 0