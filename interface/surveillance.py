#!/usr/bin/python3
# -*- coding:utf-8 -*-
import sys, hashlib, requests, json, time

LOGIN_URL = 'http://{}:11180/website/face/v2/login'
SURVEILLANCE_URL = 'http://{}:11180/website/face/v2/surveillance'
IP = sys.argv[1]
UNAME = sys.argv[2]
PASSWORD = sys.argv[3]
SESSION_ID = ''
CLUSTER_ID = ''
HEADER = {"session_id": "", "Content-Type": "application/json"}

def change_md5(pwd_md5):
    m = hashlib.md5()
    m.update(str(pwd_md5).encode('utf-8'))
    return m.hexdigest()

def get_current_timestamp():
    time_stamp = time.time()
    time_stamp_format = str(time_stamp).split('.')
    return time_stamp_format[-1]

def get_machine_ip(machine_ip):
    split_ip = str(machine_ip).split('.')
    return split_ip[-1]

def get_login_url():
    global LOGIN_URL
    LOGIN_URL = LOGIN_URL.format(IP)
    return LOGIN_URL

def get_surveillance_url():
    global SURVEILLANCE_URL
    SURVEILLANCE_URL = SURVEILLANCE_URL.format(IP)
    return SURVEILLANCE_URL

def login():
    global SESSION_ID
    global CLUSTER_ID
    global HEADER
    payload = {'name': UNAME, 'password': change_md5(PASSWORD)}
    r = requests.post(url=get_login_url(), json=payload)
    result = r.json()
    if result["rtn"] != 0:
        print(result["message"])
    else:
        SESSION_ID = result['session_id']
        CLUSTER_ID = result['cluster_id']
        HEADER['session_id'] = result['session_id']
        print(UNAME + " Login success !, Session_id: " + SESSION_ID)
        return str(SESSION_ID)

def create_surveillance_website(sur_name=''):
    global SESSION_ID
    global CLUSTER_ID
    global HEADER
    if sur_name == '':
        sur_name = get_machine_ip(IP) + '_surveillance_' + get_current_timestamp()
    payload = {
        "surveillance": {
            "enabled": True,
            "name": sur_name,
            "cluster_id": "txwl7030_61_1589506815",
            "threshold": 90,
            "repository_list": ["3@txwl7030_61_1589506815"],
            "administrative_division_list": [],
            "camera_list": ["0@txwl7030_61_1589506815"]
	    }
    }
    r = requests.post(get_surveillance_url(), json=payload, headers=HEADER)
    result = r.json()
    if result['rtn'] != 0:
        print('Create Surveillance Failed!!!!', result["message"])
        return []
    else:
        print('Surveillance : ' + sur_name + ' Create Succ!')

if __name__ == '__main__':
    login()
    create_surveillance_website()
