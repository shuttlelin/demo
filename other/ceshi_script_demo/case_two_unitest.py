#!/usr/bin/python3
# -*- coding:utf-8 -*-

import requests, unittest


class Case_Two(unittest.TestCase):
    def test_case_two(self):
        url = 'http://139.199.132.220:8000/event/weather/getWeather/'
        data = {"theCityCode": 99}
        response = requests.post(url=url, data=data, headers={'Content-Type': 'application/json'})
        # dic = response.json()
        # print(dic.get('error_code'))
        # 增加断言
        self.assertEqual(response.json().get('error_code'), 10002, '错误码不为10002')
        print('城市id不存在，流程正确')


# if __name__ == '__main__':
#    unittest.main()
