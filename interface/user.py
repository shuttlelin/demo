#!/usr/bin/python3
# -*- coding:utf-8 -*-
from faker import Faker
from interface.common.utils import md5_str

LOGIN_URL = 'http://{}:11180/website/face/v2/login'
USER_URL = 'http://{}:11180/website/face/v2/user'
USER_ADVANCE_URL = 'http://{}:11180/website/face/v2/user/cluster_level'
IP = sys.argv[1]
UNAME = sys.argv[2]
PASSWORD = sys.argv[3]
SESSION_ID = ''
CLUSTER_ID = ''
HEADER = {"session_id": "", "Content-Type": "application/json"}
f = Faker(locale='zh_CN')

def get_login_url():
    global LOGIN_URL
    LOGIN_URL = LOGIN_URL.format(IP)
    return LOGIN_URL

def get_user_url():
    global USER_URL
    USER_URL = USER_URL.format(IP)
    return USER_URL

def get_update_advance_user_url():
    global USER_ADVANCE_URL
    USER_ADVANCE_URL = USER_ADVANCE_URL.format(IP)
    return USER_ADVANCE_URL

def login():
    global SESSION_ID
    global CLUSTER_ID
    global HEADER
    payload = {'name': UNAME, 'password': md5_str(PASSWORD)}
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

def add_user():
    global HEADER
    payload = {
        "name": "userA",
        "password": "eabd8ce9404507aa8c22714d3f5eada9",
        "predecessor_id": "13@MTS_84_1577276958",
        "roleId": 3,
        "meta": {
            "realName": f.name()
        }
    }
    r = requests.post(get_user_url(), json=payload, headers=HEADER)
    result = r.json()
    if result["rtn"] != 0:
        print()
        print('Creat User Failed!!!: ', result["message"])
        return []
    else:
        print('Creat User : ' + result["id"] + ' Succ!')
        return result["id"]

def update_user(u_id):
    global HEADER
    payload = {
        'user_id': u_id
    }
    r = requests.put(get_update_advance_user_url(), json=payload, headers=HEADER)
    result = r.json()
    if result["rtn"] != 0:
        print('Update User Failed!!!!: ', result["message"])
        return []
    else:
        print('Update User : ' + u_id + ' Succ!')

if __name__ == '__mian__':
    uid = add_user()
    update_user(uid)
