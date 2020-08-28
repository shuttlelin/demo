#!/usr/bin/python3
# -*- coding:utf-8 -*-
import pytest

class TestConftestDemo:
    @pytest.mark.usefixtures("no_take_params_way_one")
    def test_get_no_take_params_way(self, take_params):
        """
        不带参数的2中方式: 
        1. 使用 pytest.mark.usefixtures 调用
        2. ()内调用
        """
        take_params.no_take_params_way_two()
        print('调用conftest中的不带参数的2种方法')

    def test_get_take_params_way(self, take_params):
        """
        带参数的调用方式: 
        1. 只能在()内调用
        """
        take_params.take_param('Aeljinh')
        print("调用conftest中的带参数的方法")

    def test_get_data_read_way(self, read_data):
        print("调用conftest中的数据准备及清理的方法")

    @pytest.mark.parametrize('params', [1, 2.5, 'abcd'])
    def test_parametrize_1(self, params):
        print('\n读取参数:' , params)

    # @pytest.mark.xfail
    @pytest.mark.parametrize("expected, actual", [('3+5', 8), ('6-3', 3), pytest.param('2*3', 7, marks=pytest.mark.xfail)])
    def test_parametrize_2(self, expected, actual):
        """
        xfail指定预期失败的case: 
        1. @pytest.mark.xfail  --> ('2*3', 7)
        2. pytest.param('2*3', 7, marks=pytest.mark.xfail)
        """
        assert eval(expected) == actual

    params = [(1, int), (1.1, float), ('1aA', str)]
    @pytest.mark.parametrize('val, val_type', params)
    def test_parametrize_3(self, val, val_type):
        assert type(val) == val_type

    def test_get_set_default_params(self, defaultparam):
        print('调用conftest中的默认的参数')

