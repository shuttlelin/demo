#!/usr/bin/python3
# -*- coding:utf-8 -*-
import sys, hashlib, requests, json, time
from common.comm import get_yesterday_timestamp, get_today_zero_timestamp

LOGIN_URL = 'http://{}:11180/website/face/v2/login'
TRACK_URL = " http://{}:7700/face/v1/framework/track/query"
ALERT_URL = "http://{}:7700/face/v1/framework/surveillance/query"
IP = sys.argv[1]
UNAME = sys.argv[2]
PASSWORD = sys.argv[3]
# OPERATION = sys.argv[4]
SESSION_ID = ''
CLUSTER_ID = ''
HEADER = {"session_id": "", "Content-Type": "application/json"}
CAMERA_ID = 12
SURVEILLANCE_ID = 1


def md5(raw_str):
    m = hashlib.md5()
    m.update(str(raw_str).encode('utf-8'))
    return m.hexdigest()


def get_login_url():
    global LOGIN_URL
    LOGIN_URL = LOGIN_URL.format(IP)
    return LOGIN_URL


def get_track_url():
    global TRACK_URL
    TRACK_URL = TRACK_URL.format(IP)
    return TRACK_URL


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


def get_all_track():
    global SESSION_ID
    global CLUSTER_ID
    payload = {
        "cluster_id": CLUSTER_ID,
        "fields": [],
        "condition": {},
        "order": {"timestamp": -1},
        "start": 0,
        "limit": 10000
    }
    response = requests.post(get_track_url(), data=json.dumps(payload), headers=HEADER)
    result = response.json()
    if result['rtn'] != 0:
        print(result['message'])
    else:
        print("总的过人数 : ", result['total'])


def get_track_by_camera():
    global SESSION_ID
    global CLUSTER_ID
    payload = {
        "cluster_id": CLUSTER_ID,
        "fields": [],
        "condition": {
            "camera_id": CAMERA_ID
        },
        "order": {"timestamp": -1},
        "start": 0,
        "limit": 10000
    }
    response = requests.post(get_track_url(), data=json.dumps(payload), headers=HEADER)
    result = response.json()
    if result['rtn'] != 0:
        print(result['message'])
    else:
        print("Devices_id = " + str(CAMERA_ID) + " 的抓拍数 ：", result['total'])


def get_track_by_cid_time(star_time, end_time):
    global SESSION_ID
    global CLUSTER_ID
    payload = {
        "cluster_id": CLUSTER_ID,
        "fields": [],
        "condition": {
            "camera_id": CAMERA_ID,
            "timestamp": {"$gte": star_time, "$lte": end_time}
        },
        "order": {"timestamp": -1},
        "start": 0,
        "limit": 100000000
    }
    response = requests.post(get_track_url(), data=json.dumps(payload), headers=HEADER)
    result = response.json()
    if result['rtn'] != 0:
        print(result['message'])
    else:
        print("Devices_id = " + str(CAMERA_ID) + " 的昨日抓拍数 ：", result['total'])


def get_all_alert():
    global SESSION_ID
    global CLUSTER_ID
    payload = {
        "cluster_id": CLUSTER_ID,
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
        print("总的预警数 : ", result['total'])


def get_alert_by_camera():
    global SESSION_ID
    global CLUSTER_ID
    payload = {
        "cluster_id": CLUSTER_ID,
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
        print("Devices_id = " + str(CAMERA_ID) + " 的今日预警数 ：", result['total'])


def get_alert_by_cid_time(star_time, end_time):
    global SESSION_ID
    global CLUSTER_ID
    payload = {
        "cluster_id": CLUSTER_ID,
        "fields": [],
        "condition": {
            "camera_id": str(CAMERA_ID) + "@MTS_212_1582704597",
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
        print("Devices_id = " + str(CAMERA_ID) + " 的昨日预警数 ：", result['total'])


def get_tody_alert_count(star_time, end_time):
    global SESSION_ID
    global CLUSTER_ID
    payload = {
        "cluster_id": CLUSTER_ID,
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
        print("今日预警总数 ：", result['total'])


def get_surveillance_alert_count():
    global SESSION_ID
    global CLUSTER_ID
    payload = {
        "cluster_id": CLUSTER_ID,
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
        print("Surveillance_id = " + str(SURVEILLANCE_ID), " 的今日预警数 ：", result['total'])


if __name__ == '__main__':
    login()
    print('------------获取抓拍数------------')
    get_all_track()  # 获取所有的过人数据
    get_track_by_camera()  # 获取某个摄像头的过人数据
    yes_timestamp = get_yesterday_timestamp()
    get_track_by_cid_time(yes_timestamp[0], yes_timestamp[1])  # 获取昨日某个设备的过人数据
    print('------------获取预警数------------')
    get_all_alert()  # 获取所有的预警数据
    get_alert_by_camera()  # 获取某个摄像头预警数
    yes_timestamp = get_yesterday_timestamp()
    get_alert_by_cid_time(yes_timestamp[0], yes_timestamp[1])  # 获取某个设备昨日预警数
    get_tody_alert_count(get_today_zero_timestamp(), int(time.time()))  # 获取今日预警数
    get_surveillance_alert_count()  # 获取某个布控的预警数
