#!/usr/bin/python3
# -*- coding:utf-8 -*-
import sys, hashlib, requests, json, time
from common.comm import get_today_zero_timestamp, get_yesterday_timestamp

LOGIN_URL = 'http://{}:11180/website/face/v2/login'
ALERT_URL = "http://{}:7700/face/v1/framework/surveillance/query"
IP = sys.argv[1]
UNAME = sys.argv[2]
PASSWORD = sys.argv[3]
OPERATION = sys.argv[4]
SESSION_ID = ''
CLUSTER_ID = ''
HEADER = {"session_id": "", "Content-Type": "application/json"}
CAMERA_ID = 1
SURVEILLANCE_ID = 1


def md5(raw_str):
    m = hashlib.md5()
    m.update(str(raw_str).encode('utf-8'))
    return m.hexdigest()


def get_login_url():
    global LOGIN_URL
    LOGIN_URL = LOGIN_URL.format(IP)
    return LOGIN_URL


def get_alert_url():
    global ALERT_URL
    ALERT_URL = ALERT_URL.format(IP)
    return ALERT_URL


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
        print("Login success with: " + UNAME + " ; The session_id is: " + SESSION_ID)
        return str(SESSION_ID)


def get_all_alert():
    global SESSION_ID
    global CLUSTER_ID
    payload = {
        "cluster_id": "MTS_212_1582704597",
        "fields": [],
        "condition": {},
        "order": {"timestamp": -1},
        "start": 0,
        "limit": 100000000
    }
    response = requests.post(get_alert_url(), data=json.dumps(payload), headers=HEADER)
    result = response.json()
    if result['rtn'] != 0:
        print(result['message'])
    else:
        print("Select Succ! All Alert Total : ", result['total'])


def get_alert_by_camera():
    global SESSION_ID
    global CLUSTER_ID
    payload = {
        "cluster_id": "MTS_212_1582704597",
        "fields": [],
        "condition": {
            "camera_id": "%d@MTS_212_1582704597" % CAMERA_ID
        },
        "order": {"timestamp": -1},
        "start": 0,
        "limit": 10000
    }
    response = requests.post(get_alert_url(), data=json.dumps(payload), headers=HEADER)
    result = response.json()
    if result['rtn'] != 0:
        print(result['message'])
    else:
        print("Select Succ! Devices_id : " + str(CAMERA_ID) + " 's Alert Total ：", result['total'])


def get_alert_by_cid_time(cid, star_time, end_time):
    global SESSION_ID
    global CLUSTER_ID
    payload = {
        "cluster_id": "MTS_212_1582704597",
        "fields": [],
        "condition": {
            "camera_id": cid,
            "timestamp": {"$gte": star_time, "$lte": end_time}
        },
        "order": {"timestamp": -1},
        "start": 0,
        "limit": 100000000
    }
    response = requests.post(get_alert_url(), data=json.dumps(payload), headers=HEADER)
    result = response.json()
    if result['rtn'] != 0:
        print(result['message'])
    else:
        print("Select Succ! Devices_id : " + str(CAMERA_ID) + " 's Yesterday Alert Count ：", result['total'])


def get_tody_alert_count(star_time, end_time):
    global SESSION_ID
    global CLUSTER_ID
    payload = {
        "cluster_id": "MTS_212_1582704597",
        "fields": [],
        "condition": {
            "timestamp": {"$gte": star_time, "$lte": end_time}
        },
        "order": {"timestamp": -1},
        "start": 0,
        "limit": 100000000
    }
    response = requests.post(get_alert_url(), data=json.dumps(payload), headers=HEADER)
    result = response.json()
    if result['rtn'] != 0:
        print(result['message'])
    else:
        print("Select Succ! Tody Alert Count ：", result['total'])


def get_surveillance_alert_count():
    global SESSION_ID
    global CLUSTER_ID
    payload = {
        "cluster_id": "MTS_212_1582704597",
        "fields": [],
        "condition": {
            "surveillance_id": SURVEILLANCE_ID
        },
        "order": {"timestamp": -1},
        "start": 0,
        "limit": 100000000
    }
    response = requests.post(get_alert_url(), data=json.dumps(payload), headers=HEADER)
    result = response.json()
    if result['rtn'] != 0:
        print(result['message'])
    else:
        print("Select Succ! Tody Alert Count ：", result['total'])


if __name__ == '__main__':
    login()
    if OPERATION == "1":  # 获取所有的预警数据
        get_all_alert()
    elif OPERATION == "2":  # 获取某个摄像头预警数
        get_alert_by_camera()
    elif OPERATION == "3":  # 获取某个设备昨日预警数
        cid = "%d@MTS_212_1582704597" % CAMERA_ID
        yes_timestamp = get_yesterday_timestamp()
        get_alert_by_cid_time(cid, yes_timestamp[0], yes_timestamp[1])
    elif OPERATION == "4":  # 获取今日预警数
        get_tody_alert_count(get_today_zero_timestamp(), int(time.time()))
    elif OPERATION == "5":  # 获取某个布控的预警数
        get_surveillance_alert_count()
