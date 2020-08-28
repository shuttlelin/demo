#!/usr/bin/python3
# -*- coding:utf-8 -*-
import os, sys, hashlib, requests, datetime, random, json
from faker import Faker
from requests_toolbelt import MultipartEncoder
from utils.file_common import read_file_dir, read_file_name

BASE_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
DATA_PATH = os.path.join(BASE_PATH, 'img\\')
# 适用 2001040模型
LOGIN_URL = "http://{}:11180/website/face/v2/login"
# 2.1.4及之前的端口为30084；2.1.5端口为9704
MONTO_URL = "http://{}:30084/v1/dynamicRepos/subjects"
IP = sys.argv[1]
UNAME = sys.argv[2]
PASSWORD = sys.argv[3]
camera_id = sys.argv[4]
SESSION_ID = ''
CLUSTER_ID = ''
HEADER = {"session_id": "", "Content-Type": "application/json"}
monto = DATA_PATH + "featureBinary_master"  # motor, featureBinary_master-1002540
monto_img = read_file_dir(DATA_PATH + 'car')[5]
monto_scene = read_file_dir(DATA_PATH + 'car_scene')[5]
monto_num = read_file_name(DATA_PATH + 'car')[5]
f = Faker(locale='zh_CN')


def get_login_url():
    global LOGIN_URL
    LOGIN_URL = LOGIN_URL.format(IP)
    return LOGIN_URL


def get_monto_url():
    global MONTO_URL
    MONTO_URL = MONTO_URL.format(IP)
    return MONTO_URL


def change_md5(pwd_md5):
    m = hashlib.md5()
    m.update(str(pwd_md5).encode('utf-8'))
    return m.hexdigest()


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


# 转换时间为指定格式，指定时区。min_shift值可以调整时间为未来的分钟数
def date_trans(min_shift=0):
    now_time = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z')
    time_eight = datetime.datetime.strptime(now_time, '%Y-%m-%dT%H:%M:%S.000Z')
    time_zero = time_eight - datetime.timedelta(hours=8)
    if min_shift != 0:
        time_zero = time_zero + datetime.timedelta(minutes=min_shift)
    time_str = time_zero.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    return time_str


def get_all_arguments():
    vehicle_place = random.choice('京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽赣粤青藏川宁琼')
    vehicle_area = random.choice('ABCDEFGHJKLMNPQRSTUVWXYZ')
    # # 车牌号
    # vehicle_plate = vehicle_place + vehicle_area + '.' + f.password(5, False, True, True, False)
    # 车牌颜色(0, 1, 4, 3, 2, 5 / 蓝色，黄色，绿色，黑色，白色，其它)
    vehicle_plate_color = random.choice(['BLUE', 'YELLOW', 'GREEN', 'BLACK', 'WHITE', 'OTHER'])
    # 车辆颜色(1, 3, 2, 8, 7, 4, 6, 5, 0, 9 / 黑色，灰色，白色，红色，棕色，蓝色，黄色，绿色，紫色，粉色)
    vehicle_body_color = random.choice(['BLACK', 'GREY', 'WHITE', 'RED', 'BROWN', 'BLUE', 'YELLOW', 'GREEN', 'VIOLET', 'PINK'])
    # 车辆行驶方向
    vehicle_direction = random.choice(['向前', '向左前', '向左', '向左后', '向后', '向右后', '向右', '向右前'])
    # 车辆品牌()
    vehicle_category = random.choice(['SUV', '宝马', '比亚迪', '大众', '奔驰', '保时捷', '本田', '法拉利', '哈佛', '兰博基尼', '劳斯莱斯', '别克'])
    # 车辆类型(0, 1, 2, 3, 4, 5, 6, 7 / 大型客车，中型客车，卡车，小货车，轿车，面包车，SUV，其它)
    vehicle_type = random.choice([0, 1, 2, 3, 4, 5, 6, 7])
    # 车辆年款(品牌、车型)
    vehicle_year_brand = random.choice(['013200010001'])
    print('车牌号: ', monto_num, '；车牌颜色: ', vehicle_plate_color, '；车辆颜色', vehicle_body_color)
    return ([{
        "parts": {
            "MOTOR_VEHICLE": {
                "feature": {"content": "motor"},
                "model":"2001040",  # 极速斧头；1002540-马里奥
                "quality": 0.9,
                "crop": {
                    "rect": {"x": 620, "y": 400, "w": 400, "h": 400},
                    "image": {"content": "xiaotu"}
                },
                "attrs": {
                    "device": camera_id,
                    "motorVehicleCategory": "SUV",  # 车辆类型
                    "motorVehicleColor": "WHITE",  # 车辆颜色
                    "motorVehicleDirection": "BACK",  # 车辆朝向
                    "motorVehicleBrandName": "0132",  # 品牌：0049-宝马，0140-奥迪，0238保时捷
                    "motorVehicleSubbrand": "01320001",  # 车型
                    "motorVehicleYearBrand": "013200010001",  # 年款
                    "motorVehiclePlateType": "BLUE",  #
                    "motorVehiclePlateColor": vehicle_plate_color,  # 车牌颜色
                    "motorVehicleLicensePlate": monto_num  # 车牌号
                }
            }
        },
        "attrs": {
            "device": camera_id,
            "externalId": "P001",
            "clusterId": CLUSTER_ID
        },
        "creationTime": date_trans(),
        "sceneImage": {"content": "scene_photos"}
    }])


def _file(arguments):
    upload_file = MultipartEncoder(
        fields={
            'file': ('motor', open(monto, 'rb'), 'text/plain'),
            'image': ('xiaotu', open(monto_img, 'rb'), 'image/jpeg'),
            'scene_image': ('scene_photos', open(monto_scene, 'rb'), 'image/jpeg'),
            'arguments': json.dumps(arguments)
        }
    )
    return upload_file


def monto_image_flow():
    global SESSION_ID
    vehicle_info = get_all_arguments()
    upload_file = _file(vehicle_info)
    header = {"session_id": SESSION_ID, 'Content-Type': upload_file.content_type}
    r = requests.post(get_monto_url(), data=upload_file, headers=header)
    result = r.json()
    print(result)
    # if result['status'] != 200:
    #     print(result)
    # else:
    #     print(result['ret'])


# python .\interface\image_flow_vehicle.py 10.40.86.177 admin admin123 camera_id
if __name__ == '__main__':
    # a = get_all_arguments()
    # print(a)
    login()
    monto_image_flow()
