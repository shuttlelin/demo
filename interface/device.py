#!/usr/bin/python3
# -*- coding:utf-8 -*-
import requests, hashlib, time, sys, csv

LOGIN_URL = 'http://{}:11180/website/face/v2/login'
Device_URL = 'http://{}:7700/face/v1/framework/face_video/camera'
IP = sys.argv[1]
UNAME = sys.argv[2]
PASSWORD = sys.argv[3]
SESSION_ID = ''
CLUSTER_ID = ''
HEADER = {"session_id": "", "Content-Type": "application/json"}
DEVICES_ID = []
CAMERA_NUM = 0
CAPTURE_NUM = 0
file_path = './tools/data/camera_list.csv'


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

def get_device_url():
    global Device_URL
    Device_URL = Device_URL.format(IP)
    return Device_URL

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

def get_device_meta():
    camera_meta_list = []
    global CAMERA_NUM
    global CAPTURE_NUM
    with open(file_path, encoding='utf-8') as f:
        content = csv.reader(f)
        for row in content:
            if content.line_num == 1:
                continue
            elif content.line_num == 2:
                continue
            count = 1
            need_create_device_num = int(row[12])
            while count <= need_create_device_num:
                device_meta = {}

                province = str(row[0])  # 省/直辖市
                city = str(row[1])  # 市/市辖区
                county = str(row[2])  # 县/区
                town = str(row[3])  # 镇/街道
                village = str(row[4])
                custom_region = str(row[5])
                device_type = str(row[6])  # 设备类型
                stream_address = str(row[7])  # 取流地址
                barrier_type = str(row[8])  # 卡口类型
                identifying_content = str(row[9])  # 识别内容
                longitude = str(row[10])  # 经度
                latitude = str(row[11])  # 纬度
                device_meta['cluster_id'] = CLUSTER_ID
                if device_type == "":
                    device_meta['type'] = 0
                    camera_num = CAMERA_NUM + 1
                    name = get_machine_ip(IP) + '_camera_' + str(camera_num) + get_current_timestamp()
                    CAMERA_NUM += 1
                elif (int(device_type) >= 0) & (int(device_type) < 10000):
                    device_meta['type'] = int(device_type)
                    camera_num = CAMERA_NUM + 1
                    if identifying_content == "1":
                        name = get_machine_ip(IP) + '_face_' + str(camera_num) + get_current_timestamp()
                    elif identifying_content == "2":
                        name = get_machine_ip(IP) + '_face+body_' + str(camera_num) + get_current_timestamp()
                    elif identifying_content == "3":
                        name = get_machine_ip(IP) + '_body_' + str(camera_num) + get_current_timestamp()
                    elif identifying_content == "6":
                        name = get_machine_ip(IP) + '_face+body+non-vehicle_' + str(camera_num) + get_current_timestamp()
                    elif identifying_content == "8":
                        name = get_machine_ip(IP) + '_vehicle_' + str(camera_num) + get_current_timestamp()
                    elif identifying_content == "13":
                        name = get_machine_ip(IP) + '_face+non-vehicle+vehicle_' + str(camera_num) + get_current_timestamp()
                    elif identifying_content == "14":
                        name = get_machine_ip(IP) + '_face+body+non-vehicle+vehicle_' + str(camera_num) + get_current_timestamp()
                    CAMERA_NUM += 1
                else:
                    device_meta['type'] = int(device_type)
                    capture_num = CAPTURE_NUM + 1
                    name = get_machine_ip(IP) + '_capture_' + str(capture_num) + get_current_timestamp()
                    CAPTURE_NUM += 1
                device_meta['name'] = name
                if stream_address == "":
                    device_meta['url'] = "rtsp://10.40.46.23:31000/proxyStream"
                else:
                    device_meta['url'] = stream_address
                device_meta['checkpoint_type'] = int(barrier_type)
                device_meta['identification_type'] = int(identifying_content)
                device_meta['meta'] = {}
                if longitude == "":
                    device_meta['meta']['GEOGRAPHY_X'] = "121.123"
                else:
                    device_meta['meta']['GEOGRAPHY_X'] = longitude
                if latitude == "":
                    device_meta['meta']['GEOGRAPHY_Y'] = "31.123"
                else:
                    device_meta['meta']['GEOGRAPHY_Y'] = latitude
                device_meta['administrative_division'] = {}
                if province == "":
                    device_meta['administrative_division']['province'] = "11"
                else:
                    device_meta['administrative_division']['province'] = province
                if city == "":
                    device_meta['administrative_division']['city'] = "01"
                else:
                    device_meta['administrative_division']['city'] = city
                device_meta['administrative_division']['county'] = county
                device_meta['administrative_division']['town'] = town
                device_meta['administrative_division']['village'] = village
                if custom_region == "":
                    device_meta['administrative_division']['custom_region_id'] = -1
                else:
                    device_meta['administrative_division']['custom_region_id'] = custom_region
                device_meta['administrative_display_name']['province_name'] = '上海市'
                device_meta['administrative_display_name']['city_name'] = '市辖区'
                device_meta['administrative_display_name']['county_name'] = '长宁区'
                camera_meta_list.append(device_meta)
                count += 1
        return camera_meta_list

def create_device():
    global SESSION_ID
    global CLUSTER_ID
    global HEADER
    global DEVICES_ID
    device_list_meta = get_device_meta()
    DEVICES_ID = []
    for device_info in device_list_meta:
        r = requests.post(get_device_url(), json=device_info, headers=HEADER)
        result = r.json()
        if result["rtn"] != 0:
            print('Device Create Failed!!!!', result["message"])
            return []
        else:
            print('Device : ' + device_info['name'] + ' Create Succ!')
            DEVICES_ID.append(result["id"])

if __name__ == '__main__':
    login()
    create_device()
