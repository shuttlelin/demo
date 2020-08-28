#!/usr/bin/python3
# -*- coding:utf-8 -*-
import requests, unittest


class Case_One(unittest.TestCase):
    def test_case_one(self):
        url = 'http://139.199.132.220:8000/event/weather/getWeather/'
        data = {"theCityCode": 1}
        response = requests.post(url=url, data=data, headers={'Content-Type': 'application/json'})
        dic = response.json()
        # print(dic.get('error_code'))
        #增加断言(检查点)
        self.assertEqual(dic.get('cid'), '02', '城市id返回错误') # 实际结果，预期结果，错误日志(不相等才会输出)
        self.assertEqual(dic.get('error_code'), '0', '错误码不为0')
        print('接口正常流程正确')

# if __name__ == '__main__':
#    unittest.main()
