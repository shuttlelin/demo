#!/usr/bin/python3
# -*- coding:utf-8 -*-

import json, unittest, requests


'''
因为在unittest中，一旦某个测试方法中的断言失败，后续的断言都不会被执行[，所以只能打印第一个结果]
断言一旦失败之后测试方法就会结束运行，所以一般来说1个测试方法推荐只有1个断言
如果一个测试方法里面必须要有多个断言，那么要确保前面的断言失败之后，后面的断言就算不运行也不会影响测试的范围和结果
for循环中的断言一旦失败，for循环就退出了
上面演示的测试用例写法其实具备了一定的数据驱动测试的思想
命令行指定只运行某个用例：python -m unittest junit_test.PasswordTeseCase -v
    -v：获得更详细的输出
'''

# 一 基本用法
# class TestStirngMethods(unittest.TestCase):
#     def test_upper(self):
#         # 判断预期结果
#         self.assertEquals('foo'.upper(), 'FOO')
#     def test_isupser(self):
#         # 是非判断
#         self.assertTrue('FOO'.isupper())
#         self.assertFalse('Foo'.isupper())
#     def test_split(self):
#         str = 'hello word'
#         self.assertEqual(str.split(), ['hello', 'word'])
#         # 判断预期的异常是否有被抛出
#         with self.assertRaises(TypeError):
#             str.split(2)

# 二 实例，测试弱密码
# class PasswordTeseCase(unittest.TestCase):
#     def setUp(self):
#         print('setUp.......')
#         self.test_data = [
#             dict(name='jack', passwd='Iloverose'),
#             dict(name='rose', passwd='Ilovejack'),
#             dict(name='tom', passwd='password123'),
#             dict(name='jerrf', passwd='password')
#         ]
#     def test_week_password(self):
#         for data in self.test_data:
#             pwd = data['passwd']
#             self.assertTrue(len(pwd) >= 6)
#             # 因为在unittest中，一旦某个测试方法中的断言失败，后续的断言都不会被执行[，所以只能打印第一个结果]
#             msg = "user %s has a weak password" % (data['name'])
#             self.assertTrue(pwd != 'password', msg)
#             self.assertTrue(pwd != 'password123', msg)
#     def test_dummy(self):
#         pass

# 三 实例，读取测试数据并测试弱密码
# class PasswordWithJsonTeseCase(unittest.TestCase):
#     # file_path = 'user_data.json'
#     # def setUp(self):
#     #     print('setUp.........')
#     #     self.test_data = json.loads(open(self.file_path).read())
#     # 优化
#     @classmethod
#     # 在setUpClass方法中可以直接设置变量，比如kls.test_data = json.loads(f.read())，在其他测试方法中可以被访问
#     def setUpClass(kls):
#         file_path = 'user_data.json'
#         print('before all test methods')
#         # 使用open 方法的with模式可以在读取文件后自动关闭文件
#         with open(file_path) as f:
#             kls.test_data = json.loads(f.read())
#     def test_weak_password(self):
#         for data in self.test_data:
#             pwd = data['passwd']
#             self.assertTrue(len(pwd) >= 6)
#             # 因为在unittest中，一旦某个测试方法中的断言失败，后续的断言都不会被执行[，所以只能打印第一个结果]
#             msg = "user %s has a weak password" % (data['name'])
#             self.assertTrue(pwd != 'password', msg)
#             self.assertTrue(pwd != 'password123', msg)

# 四 实例，找出所有是弱密码的用户
# class WeakPasswordTeseCase(unittest.TestCase):
#     @classmethod
#     def setUpClass(kls):
#         file_path = 'D:\\python\demo\\pythontest\\user_data.json'
#         print('before all test method')
#         with open(file_path) as f:
#             kls.test_data = json.loads(f.read())
#     def test_week_password(self):
#         res = True
#         msg = []
#         for data in self.test_data:
#             pwd = data['passwd']
#             tmp_res = True
#             tmp_res = tmp_res and (len(pwd) >= 6)
#             tmp_res = tmp_res and (pwd != 'password')
#             tmp_res = tmp_res and (pwd != 'password123')
#             if not tmp_res:
#                 msg.append('user %s has a weak password --> %s' % (data['name'], data['passwd']))
#             res = res and tmp_res
#         self.assertTrue(res, '\n'.join(msg))

# 五 断言异常
# class DivZeroTestCase(unittest.TestCase):
#     def test_should_raise_exception(self):
#         with self.assertRaises(ZeroDivisionError):
#             1 / 0

# 3A原则（Arrange-数据准备、Act-调用接口，输入数据、Assert-断言）
# class StringTestCase(unittest.TestCase):
#     # 每个测试用例执行之前都会执行一次，是做数据初始化的好地方
#     def setUp(self):
#         # Arrange
#         self.test_string = 'This is a string' # 被测对象
#     # 测试方法，就是一个测试用例
#     def testUpper(self):
#         # Act Assert
#         self.assertEqual('THIS IS A STRING', self.test_string.upper()) # 断言方法，作用是如果第一个参数跟第二个参数相等，那么用例通过，否则用例失败

# 接口自动化
class V2exAPITestCase(unittest.TestCase):
    def test_node_api(self):
        # postman调用http://www.v2ex.com/api/nodes/show.json?name=python，点击code选择python request生成的
        url = "http://www.v2ex.com/api/nodes/show.json"
        querystring = {"name":"python"}
        # headers = {
        #     'cache-control': "no-cache",
        #     'postman-token': "6f3a0962-a17f-7f84-fddd-ef1eff8cf921"
        #     }
        # response = requests.request("GET", url, headers=headers, params=querystring)
        response = requests.request("GET", url, params=querystring).json()
        self.assertEqual(response['name'], 'python')
        self.assertEqual(response['id'], 90)
        # print(response.text)

if __name__ == '__main__':
    # 最简单的运行用例的方式
    unittest.main()
    # 每个方法都会显示ok
    # suite = unittest.TestLoader().loadTestsFromTestCase(TestStirngMethods)
    # unittest.TextTestRunner(verbosity=2).run(suite)