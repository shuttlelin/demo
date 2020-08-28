#!/usr/bin/python3
# -*- coding:utf-8 -*-

import time


def calls(text):
    def dec(f):
        # def wrapper(name):
        #     print(name, text, '%s()' % func.__name__)
        def wrapper(*args, **kwargs):
            # print(time.strftime('%Y-%m-%d %H:%M:%S'), f(*args, **kwargs), '%s %s()' % (text, f.__name__))
            print('%s，%s %s %s()' % (time.strftime('%Y-%m-%d %H:%M:%S'), f(*args, **kwargs), text, f.__name__))
            return f
        return wrapper
    return dec


@calls("hehe")
def call(name):
    # print(name) # 这里使用print 上面的f(*args, **kwargs)就要放到return中会换行输出
    return name


call('shulin.deng')  # call() ==> calls("execute")(call)()
