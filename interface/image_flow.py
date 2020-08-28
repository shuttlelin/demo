#!/usr/bin/python3
# -*- coding:utf-8 -*-
import os, sys, time, requests, json
from utils.common import picture_trans_base
from utils.file_common import read_file_dir
from ast import literal_eval
"""
6030模型：不支持解析，需要带特征（rec_feature_base64）
    2.1.3
7030模型：支持解析，不需要带特征
    2.1.4
"""
IMAGE_FLOW = 'http://{}:21100/face/v1/face_image_flow'

BASE_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
DATA_PATH = os.path.join(BASE_PATH, 'img\\')

if len(sys.argv) < 4:
    sys.exit("缺少参数")
if len(sys.argv) >= 4:
    IP = sys.argv[1]
    CAMER_ID = sys.argv[2]
    OPERATOR = sys.argv[3]
if len(sys.argv) == 5:
    IMG_PATH = sys.argv[4]
if len(sys.argv) > 5:
    print("参数过多")
FACE_IMG = read_file_dir(DATA_PATH + 'face')[2]
BODY_IMG = read_file_dir(DATA_PATH + 'img\\body')[6]
SCAN_IMG = read_file_dir(DATA_PATH + 'scene')[2]


def get_image_flow_url():
    global IMAGE_FLOW
    IMAGE_FLOW = IMAGE_FLOW.format(IP)
    return IMAGE_FLOW


def face_image():
    payload = {
        "mode": 1,  # 识别人脸
        "face_image_content_base64": picture_trans_base(FACE_IMG),
        "picture_image_content_base64": picture_trans_base(SCAN_IMG),
        "camera_id": int(CAMER_ID),
        "timestamp": int(time.time()),
        "force_input": True
    }
    response = requests.post(get_image_flow_url(), data=json.dumps(payload))
    result = response.json()
    if result['rtn'] == 0:
        print(result['message'])
    else:
        print(result)


def face_body_image():
    payload = {
        "mode": 3,  # 识别人脸+人体
        "face_image_content_base64": picture_trans_base(FACE_IMG),
        "pedestrian_image_content_base64": picture_trans_base(BODY_IMG),
        "picture_image_content_base64": picture_trans_base(SCAN_IMG),
        "camera_id": int(CAMER_ID),
        # "face_rect": {"h": 109, "w": 109, "x": 653, "y": 272},
        # "pedestrian_rect": {"h": 871, "w": 393, "x": 506, "y": 209},
        "rec_feature_base64": {
            "yitu_130700300_feature_base64": "FZ6U/dEa0/mNlg70RBJN/weOhe3ACsHpf2bOBmsSO/EAj5wqXgRC0m9rNt72/9c7FaGe7FMUXSxHkivBFAnjHca6r7GOJnlIREfPRe3W67AYsE1SccqLr8aoQELtxySjtcTAnphKhpfUO0eQ+kP7ZlMoJVGWvGBvEdqQcNZSO3GD5xWSuG5RhuAZjnfebsRtlwMBgbuFuIMV94SfVIS7npH19KMwcshZEPd8UqqNuEuf7eZEO58iSSwOXq6anZq/XdnQPBC87DPe3KU+cVtkOl3G0SzxsAHRQjjD231WfCI0q0IN9ccNAadI0O9+JmMW36SpBfPU4QidoREMXSJaCuxtZ/TT5yoGg2gM/bITtgkHjoYXyfLCFIKJ/eE0Ajng93J12rz6sN5vdu3UJPIr0+duZcyj5aHPUGbdxBrqGcDXblW8kqiRuE6hzbQPIQmwwUdFrIIPgag4A72k/c35oLGbNZx2JXGYKvCtlO/X6ZCnyyWMZZFhiBlgnYTcPNmAk4MVfFXyUXgIBo10zlPJcIX1BWxCc0Fo+jt9ZL2JuWBz6vVcMPcxWO0ObVSsqKlQYm3lTCLcIUjdWl1En9eZQFcX1TwROxE4zJJNNIkhiTBC3MUsAPcBKL4uPSR5EnkgN7+1HPb68RipgS0UbddpECRqpQzmVOEImq4dBFszWQAT+p382xrR+I+eDf1LEknwD46P6wlezeR/jfvkOgI05vd8dZqw+rLbaXbp1CvxKdXhbmU=",
            "yitupedes_1002540_feature_base64": "FZ6U/dEa0/mNlg70RBJN/weOhe3ACsHpf4D+6tfwzv3xfYnYTPRfyph3/8TE/CjA54Bj26cUuOivnNw6EhEQyyykoLeU0mVBRl3dS/Mu/7nIQUysg9pxViy1oa38y/ypt+A1nHi9iJrI3KJI5732ir/QP31rpmCJ6siFQt+/Ko+06+2JVpqvdfoLjonNmzVrgtrjcJ6CRJjkB31kQXe0mon++JXGcjJC/QmQqq2DQkuQ//S+1Y0CRj70VbOVlWBMV9otwO1TDSLGOLQohLqCyVYuwc0AXQfUv88+IYVCcNg/rFnmDNHmH1C5KQyexWThKL5dFw8iFvBkpfYGtNurC+2VmP4k5ij4mmUJ/EMKvvUBhogKOfbF6IWJ/eE0Ajng93J12rz6sN5vdu3UJPIr0+duZcyj5aHPUGbdxBvqGcjXXlW8m9qYuE9WzbwL2Am/i2JF"
        },
        "timestamp": int(time.time()),
        "force_input": True
    }
    response = requests.post(get_image_flow_url(), data=json.dumps(payload))
    result = response.json()
    if result['rtn'] == 0:
        print(result['message'])
    else:
        print(result)


def body_image():
    payload = {
        "mode": 2,  # 只识别人体
        "pedestrian_image_content_base64": picture_trans_base(BODY_IMG),
        "picture_image_content_base64": picture_trans_base(SCAN_IMG),
        "rec_feature_base64": {
            "yitupedes_1002540_feature_base64": "FZ6U/dEa0/mNlg70RBJN/weOhe3ACsHpf8z95d0F7hH3eZvIuvxU3oOPDiwy9ynf43Jjzl0Zp9BZdiEq5eEWyTCxr1iHIJJMSE8ysPk0DawwSKVXkNmFuC6VSFv4PwyyRen6kJxehZgvL4SU/lcYf6072VFuoZB/CyGdnsqpOGqX4O58qJusjvERg5knbsOffQ3+YEBrS5MQ9H1ovZq5ln8JCK3ZhyJdBBmAV15yXrac6hazL4DOTdnxs0lvaXlDpdjTxQet5TYx3FwjdaRyNrPAPtkDRQnNtDLbJ4asaSDNRVwcB8IO9UBKJg1lyZcWLFenDOPc9QOYtBTqW9ZVABdjkvkpHiAMdWkCALYTs/MFhnvow/c/6ImJ/eE0Ajng93J12rz6sN5vdu3UJPIr0+duZcyj5aHPUGbdxBvqGcjXXlW8m9qYuE9WzbwL2Am/i2JF"
        },
        "camera_id": int(CAMER_ID),
        "timestamp": int(time.time()),
        "force_input": True,
        # "rec_glasses": 0,  # 眼镜
        # "rec_gender": 1,  # 性别，1-男
        # # "rec_age": 1,
        # "rec_age_range": 1,  # 年龄，1-青年
        # "rec_upperbody_color": 0,  # 上身颜色，0-黑色、1-白色
        # "rec_sunglass": 0,  # 墨镜，0-无、1-有
        # "rec_hat": 1,  # 帽子，1-戴
        # "rec_lowerbody_color": 1,  # 下身颜色，1-黑
        # "rec_is_calling": 0,  # 打电话，0-不在、1-在
        # "rec_mask": 0,  # 口罩，0-无、1-有
        # "rec_backpack": 0,  # 背包，0-无、1-有
        # "rec_hairstyle": 0,  # 发型，0-长、1-短发
        # "rec_beard": 1,  # 胡须，1-有
        # "rec_shoulderbag": 0,  # 挎包，0-无、1-有
        # "rec_carrythings": 0,  # 领东西，0-无、1-有
        # "rec_baby_in_arms": 0,  # 抱小孩，0-不抱、1-抱
        # "rec_direction": 0  # 行人朝向，0-左、1-右
    }
        # "rec_non_motor_vehicle_category": "",
        # "rec_non_motor_vehicle_has_person": "",
        # "rec_non_motor_vehicle_multi_person": "",  # 载人数
        # "rec_non_motor_vehicle_direction": "",  # 朝向
        # "rec_non_motor_vehicle_color": "",  # 非机动车颜色
        # "rec_non_motor_vehicle_hat": "",  #
        # "rec_non_motor_vehicle_hat_style": "",
        # "has_ride_non_motor_vehicle": ""  # 是否骑车
    response = requests.post(get_image_flow_url(), data=json.dumps(payload))
    result = response.json()
    if result['rtn'] == 0:
        print(result['message'])
    else:
        print(result)


def capture_image():  # 通用
    payload = {
        "face_image_content_base64": picture_trans_base(FACE_IMG),
        "picture_image_content_base64": picture_trans_base(SCAN_IMG),
        "camera_id": int(CAMER_ID),
        "timestamp": int(time.time())
    }
    response = requests.post(get_image_flow_url(), data=json.dumps(payload))
    result = response.json()
    if result['rtn'] == 0:
        print(result['message'])
    else:
        print(result)


def mobile_device_image():  # 通用
    payload = {
        "face_image_content_base64": picture_trans_base(FACE_IMG)[0],
        "picture_image_content_base64": picture_trans_base(SCAN_IMG)[0],
        "camera_id": int(CAMER_ID),
        "timestamp": int(time.time()),
        "shot_place_full_address": "金虹桥国际中心",
        "shot_place_latitude": 31.2,
        "shot_place_longitude": 121.2
    }
    response = requests.post(get_image_flow_url(), data=json.dumps(payload))
    result = response.json()
    if result['rtn'] == 0:
        print(result['message'])
    else:
        print(result)


def capture_image_batch():
    payload = {
        "tasks": [{
            "face_image_content_base64": picture_trans_base(FACE_IMG),
            "picture_image_content_base64": picture_trans_base(SCAN_IMG),
            "camera_id": int(CAMER_ID),
            "timestamp": int(time.time())
        }]
    }
    response = requests.post(get_image_flow_url(), data=json.dumps(payload))
    result = response.json()
    if result['rtn'] == 0:
        print(result['message'])
    else:
        print(result)


def a(img_file):
    payload = {
        "mode": 1,
        "face_image_content_base64": picture_trans_base(img_file),
        "picture_image_content_base64": picture_trans_base(SCAN_IMG),
        "camera_id": int(CAMER_ID),
        "timestamp": int(time.time()),
        "force_input": True
    }
    response = requests.post(get_image_flow_url(), data=json.dumps(payload))
    result = response.json()
    if result['rtn'] == 0:
        print(result['message'])
    else:
        print(result)


def more_devices_send_image():
    global CAMER_ID
    c_id = literal_eval(CAMER_ID)
    file_path = os.listdir(DATA_PATH + IMG_PATH)
    # print(file_path)
    for f in file_path:
        # if f.find('.') != -1:  # 若目录下有其它文件则需要过滤
        #     if f.split('.')[1] in ['jpg', 'jpeg', 'jpg']:  # 只筛选出图片文件
        #         print(f)
        for CAMER_ID in range(c_id[0], c_id[1]):  # 取头不取尾
            a(DATA_PATH + IMG_PATH + f)


if __name__ == '__main__':
    # python .\interface\image_flow.py 10.40.88.61 1 1
    if OPERATOR == '1':
        face_image()
    elif OPERATOR == '2':
        face_body_image()
    elif OPERATOR == '3':
        body_image()
    elif OPERATOR == '4':
        capture_image()
    elif OPERATOR == '5':
        mobile_device_image()
    elif OPERATOR == '6':
        capture_image_batch()
    elif OPERATOR == '7':
        # python .\interface\image_flow.py 10.40.80.73 [28,30] 7 img/face/
        more_devices_send_image()
