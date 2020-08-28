#!/usr/bin/python3
# -*- coding:utf-8 -*-
import base64, hashlib
from faker import Faker
f = Faker(locale='zh_CN')


# 图片转base64
def picture_trans_base(file_path):
    with open(file_path, 'rb') as f:
        img_base = base64.b64encode(f.read()).decode('ascii')
        # base = str(img_base)
    return img_base  # base[2:-1]


# 密码加密
def md5_str(str):
    m = hashlib.new('md5')
    m.update(str.encode('utf-8'))
    return m.hexdigest()


def format_size(bytes):  # 字节转换
    try:
        bytes = float(bytes)  # 得到byte字节
        kb = bytes / 1024  # byte --> kb
    except:
        print("传入的字节格式不对")
        return "Error"
    if kb >= 1024:
        M = kb / 1024  # kb --> M
        if M >= 1024:
            G = M / 1024  # M --> G
            return "%fG" % (G)
        else:
            return "%fM" % (M)
    else:
        return "%fkb" % (kb)


if __name__ == '__main__':
    # car_base64_list = picture_trans_base('C:/workspace/automation/interface/data/img/car')
    # print(random.choice(car_base64_list))
    print(f.password(length=80, special_chars=False, digits=True, upper_case=False, lower_case=False))
