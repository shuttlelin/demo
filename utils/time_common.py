#!/usr/bin/python3
# -*- coding:utf-8 -*-
import time


def get_current_time(time_format):  # 获取当前时间
    return time.strftime(time_format, time.localtime(time.time()))


def datetime_strf_and_timestamp(strp):  # 格式转换
    time_strp = time.strptime(strp, "%Y-%m-%d %H:%M:%S")
    timestamp = int(time.mktime(time_strp))
    return timestamp
