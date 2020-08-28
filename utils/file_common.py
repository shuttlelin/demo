#!/usr/bin/python3
# -*- coding:utf-8 -*-
import os
from faker import Factory
from utils.common import format_size

fake_english = Factory().create()
fake_china = Factory().create('zh_CN')


def create_folder(folder_path):  # 创建文件夹
    is_exists = os.path.exists(folder_path)
    if not is_exists:
        try:
            os.makedirs(folder_path)
        except Exception as e:
            print('文件夹创建失败', e)
    return folder_path


def read_file_dir(file_dir):  # 读取文件路径
    image_dir = []
    for root, dirname, filename in os.walk(file_dir):
        for file in filename:
            image_dir.append(os.path.join(root, file))
    return image_dir


def read_file_name(file_dir):  # 读取文件名
    file_path = read_file_dir(file_dir)
    file_name = []
    for name in file_path:
        file_name.append(name.split('\\', 7)[-1].split('.')[0])
    return file_name


def file_rename(folder_path, language):  # 文件重命名
    file_list = os.listdir(folder_path)  # 该文件夹下所有的文件（包括文件夹）
    for files in file_list:  # 遍历所有文件/夹
        print('文件名+路径-->', files)
        id_card = fake_china.ssn()  # 身份证
        name = fake_china.name()  # 中文名
        e_name = fake_english.password(6, False, False, True, True)  # 英文名
        year = fake_china.year()  # 年
        month = fake_china.month()  # 月
        date = str(year) + str(month)  # 日
        out_id = fake_china.numerify()  # 外部id
        old_dir = os.path.join(folder_path, files)  # 原来的文件路
        if os.path.isdir(old_dir):  # 如果是文件夹则跳过
            continue
        file_name = os.path.splitext(files)[0]  # 文件名
        file_type = os.path.splitext(files)[1]  # 文件扩展名
        print('文件名：%s；扩展名：%s' % (file_name, file_type))
        # # 截取文件名中的名字
        # split_list = file_name.split('_', 4)
        # print(split_list[3])
        # new_folder_name = '1___' + str(id_card) + '_' + split_list[3] + '_' + str(date) + '_' + str(out_id)  # 使用读取本地文件名作为文件名
        new_folder_name = ''
        if language == 'chinese':
            new_folder_name = '1___' + str(id_card) + '_' + name + '_' + str(date) + '_' + str(out_id)
            # new_folder_name = '1___' + str(id_card) + '_' + file_name + '_' + str(date) + '_' + str(out_id)  # 使用读取本地文件名作为文件名
        elif language == 'enginlish':
            new_folder_name = '1___' + str(id_card) + '_' + e_name + '_' + str(date) + '_' + str(out_id)
            # new_folder_name = e_name
        print('新文件名-->', new_folder_name)
        new_dir = os.path.join(folder_path, new_folder_name + file_type)  # 新的文件路径
        os.rename(old_dir, new_dir)  # 重命名


def get_file_size(path):  # 读取文件大小
    try:
        size = os.path.getsize(path)  # 获取文件大小(字节)
        # 转换成相应的大小
        return format_size(size)
    except Exception as err:
      print(err)
