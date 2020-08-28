#!/usr/bin/python3
# -*- coding:utf-8 -*-
import pytest


@pytest.fixture()
def no_take_params_way_one():
    print("\n不带参数的方法-1")


@pytest.fixture()
def take_params():
    class ParamsClasss:
        def no_take_params_way_two(self):
            print("不带参数的方法-2")
        
        def take_param(self, uname):
            print("\n带了一个参数: ", uname)
    
    return ParamsClasss()


@pytest.fixture(scope='class')
def read_data(request):
    print('\n创建数据。。。')

    def fin():
        print('\n所有test全部执行完成后，，，删除创建的数据。。。')
    request.addfinalizer(fin)


def pytest_addoption(parser):
    parser.addoption('--defaultparams', default='admin')


@pytest.fixture(scope='session')
def defaultparam(request):
    print('\n获取设置的默认参数')
    return request.config.getoption('--defaultparams')
