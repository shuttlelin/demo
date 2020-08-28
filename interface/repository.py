#!/usr/bin/python3
# -*- coding:utf-8 -*-
import sys, hashlib, requests, json, time, os
from interface.utils import picture_trans_base
from interface.common.read_file_path import DATA_PATH
from interface.common.utils import 

LOGIN_URL = 'http://{}:11180/website/face/v2/login'
CREAT_REPOSITORY_URL = 'http://{}:11180/business/api/repository'
LOADIMG_URL = 'http://{}:11180/business/api/repository/picture/batch_single_person'
IP = sys.argv[1]
UNAME = sys.argv[2]
PASSWORD = sys.argv[3]
OPERATION = sys.argv[4]
SESSION_ID = ''
CLUSTER_ID = ''
HEADER = {"session_id": "", "Content-Type": "application/json"}
REPO_ID = []
REPO_NAME = []
FACE_IMG = DATA_PATH + 'xm031_face.jpg'

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

def get_create_repository_url():
    global CREAT_REPOSITORY_URL
    CREAT_REPOSITORY_URL = CREAT_REPOSITORY_URL.format(IP)
    return CREAT_REPOSITORY_URL

def get_import_img_url():
    global LOADIMG_URL
    LOADIMG_URL = LOADIMG_URL.format(IP)
    return LOADIMG_URL

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

def get_repository_info():
    global SESSION_ID
    global CLUSTER_ID
    global HEADER
    global REPO_ID
    global REPO_NAME
    r = requests.get(get_create_repository_url(), headers=HEADER)
    result = r.json()
    if result["rtn"] != 0:
        print('Select Repository Failed!!!!', result)
        return []
    else:
        repo_list_info = result['results']
        for i in repo_list_info:
            REPO_ID.append(i['id'])
            REPO_NAME.append(i['name'])
        return REPO_ID, REPO_NAME

def create_repository(repo_name=''):
    global SESSION_ID
    global CLUSTER_ID
    global HEADER
    global REPO_ID
    if repo_name == '':
        repo_name = get_machine_ip(IP) + '_repo_' + '_' + get_current_timestamp()
    payload = {"name": repo_name}
    r = requests.post(get_create_repository_url(), json=payload, headers=HEADER)
    result = r.json()
    if result["rtn"] != 0:
        print('Create Repository Failed!!!!', result["message"])
        return []
    else:
        print('Repository : ' + repo_name + ' Create Succ!')

def import_image():
    global SESSION_ID
    global CLUSTER_ID
    global HEADER
    payload = {
        "images": [{
            "repository_id": "10",
            "picture_image_content_base64": picture_trans_base(FACE_IMG),
            "person_id": "421799198912057894",
            "gender": 1,
            "name": "哈哈"
        }]
    }
    r = requests.get(get_import_img_url(), json=payload, headers=HEADER)
    result = r.json()
    print(result)
    # if result["rtn"] != 0:
    #     print('Create Repository Failed!!!!', result["message"])
    #     return []
    # else:
    #     print('Image Import Succ!!!!', result["message"])


if __name__ == '__main__':
    login()
    # get_repository_info()
    # print('获取repo id: ', REPO_ID)
    # print('获取repo name: ', REPO_NAME)
    if OPERATION == '1':
        create_repository()
    elif  OPERATION == '2':
        import_image()
