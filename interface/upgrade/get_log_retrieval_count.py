#!/usr/bin/python3
# -*- coding:utf-8 -*-
import sys, hashlib, requests, json, time
from common.comm import get_yes7_timestamp, get_today_zero_timestamp

LOGIN_URL = 'http://{}:11180/website/face/v2/login'
RETRIEVAL_URL = "http://{}:7700/face/v1/framework/face/log/statistic"
IP = sys.argv[1]
UNAME = sys.argv[2]
PASSWORD = sys.argv[3]
OPERATION = sys.argv[4]
SESSION_ID = ''
CLUSTER_ID = ''
HEADER = {"session_id": "", "cluster_id": "", "Content-Type": "application/json"}
USER_ID = [2]


def md5(raw_str):
    m = hashlib.md5()
    m.update(str(raw_str).encode('utf-8'))
    return m.hexdigest()


def get_login_url():
    global LOGIN_URL
    LOGIN_URL = LOGIN_URL.format(IP)
    return LOGIN_URL


def get_retrieval_url():
    global RETRIEVAL_URL
    RETRIEVAL_URL = RETRIEVAL_URL.format(IP)
    return RETRIEVAL_URL


def login():
    global SESSION_ID
    global CLUSTER_ID
    global HEADER
    print('start_login...')
    payload = {'name': UNAME, 'password': md5(PASSWORD)}
    r = requests.post(url=get_login_url(), json=payload)
    result = r.json()
    if result['rtn'] != 0:
        print(result['message'])
        return None
    else:
        SESSION_ID = result['session_id']
        CLUSTER_ID = result['cluster_id']
        HEADER['session_id'] = result['session_id']
        print("Login success with: " + UNAME + " ; The session_id is: " + SESSION_ID + " ; The cluster_id is: " + CLUSTER_ID)
        return str(SESSION_ID), str(CLUSTER_ID)


def get_log_retrieval(star_time, end_time):
    global SESSION_ID
    global CLUSTER_ID
    payload = {
        "user_ids": USER_ID,
        "timestamp_begin": star_time,
        "timestamp_end": end_time
    }
    # response = requests.request("POST", get_retrieval_url(), data=json.dumps(payload), headers=HEADER)
    response = requests.post(get_retrieval_url(), data=json.dumps(payload), headers=HEADER)
    result = response.json()
    if result['rtn'] != 0:
        print(result['message'])
    else:
        print("Select Succ! Retrieval Totals : ", result['user_results'])


if __name__ == '__main__':
    login()
    if OPERATION == "1":  # 获取近7日检索次数
        get_log_retrieval(get_yes7_timestamp(), int(time.time()))
    elif OPERATION == "2":  # 获取今日检索次数
        get_log_retrieval(get_today_zero_timestamp(), int(time.time()))
