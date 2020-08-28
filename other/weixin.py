#!/usr/bin/python3
# -*- coding:utf-8 -*-

import itchat, re, csv, matplotlib.pyplot as plt
from scipy.misc import imread
# from wordcloud import WordCloud, ImageColorGenerator


# 获取男女比例
def get_friends_sex():
    text = dict()  # 保存性别
    friends = itchat.get_friends(update=True)[0:]  # 获取好友相关信息(、、、)，返回json格式
    print('######', friends)
    male = "male"
    female = "female"
    other = "zhengli"
    for i in friends[1:]:  # 把获取到的数据通过 for 循环保存到 text 字典里【friends[0]是自己的信息，所以要从friends[1]开始】
        sex = i['Sex']
        if sex == 1:  # 男
            text[male] = text.get(male, 0) + 1
        elif sex == 2:  # 女
            text[female] = text.get(female, 0) + 1
        else:
            text[other] = text.get(other, 0) + 1
    total = len(friends[1:])
    print('好友总数：', total)
    print("男性好友：%.2f%%" % (float(text[male]) / total * 100) + '\n' +
          "女性好友：%.2f%%" % (float(text[female]) / total * 100) + '\n' +
          "不明性别好友：%.2f%%" % (float(text[other]) / total * 100))
    draw(text)  # 画柱状图


def draw(datas):
    for key in datas.keys():
        plt.bar(key, datas[key])
    plt.legend()
    plt.xlabel('sex')  # x轴的说明
    plt.ylabel('rate')  # y轴的说明
    plt.title("Gendren of Alfred's friedns")  # 总标题
    plt.show()  # 展示


# 获取微信好友数据
def get_data():
    friends = itchat.get_friends(update=True)[1:]
    file = open('test.txt', 'w', newline='', encoding="utf-8") # .csv格式的文件编码是gb18030  .txt格式的文件编码是utf-8
    write = csv.writer(file)
    write.writerow(['昵称', '备注名', '性别', '签名', '地区'])
    for friend in friends:
        nickname = friend['NickName'].strip().replace("span", "").replace("class", "").replace("emoji", "")
        remarkname = friend['RemarkName']
        sex = friend['Sex']
        if sex == 1:
            sex = '男'
        elif sex == 2:
            sex = '女'
        else:
            sex = '未知'
        sign = friend['Signature'].strip().replace("span", "").replace("class", "").replace("emoji", "")
        rep = re.compile("1f\d+\w*|[<>/=]")
        signature = rep.sub("", sign)
        province = friend['Province']
        city = friend['City']
        region = province + '-' + city
        write.writerow((nickname, remarkname, sex, signature, region))
        print(nickname, '：', remarkname, sex, signature, region)
    file.close()


# 制作词云
def draw_wordcloud():
    # 读取一个txt文件
    text = open('test.txt', 'r', encoding='utf-8').read()
    # 读入背景图片
    bg_pic = imread('3.jpg')
    '''
    生成词云
        WordCloud(font_path=None, width=400, height=200, margin=2, ranks_only=None, prefer_horizontal=0.9,mask=None, scale=1, color_func=None, max_words=200, 
        min_font_size=4, stopwords=None, random_state=None,background_color='black', max_font_size=None, font_step=1, mode='RGB', relative_scaling=0.5, regexp=None, 
        collocations=True,colormap=None, normalize_plurals=True)
            background_color : color value (default=”black”) //背景颜色，如background_color='white',背景颜色为白色。
            font_path : string //字体路径，需要展现什么字体就把该字体路径+后缀名写上，如：font_path = '黑体.ttf'
            mask : nd-array or None (default=None) //如果参数为空，则使用二维遮罩绘制词云。如果 mask 非空，设置的宽高值将被忽略，遮罩形状被 mask 取代。
                除全白（#FFFFFF）的部分将不会绘制，其余部分会用于绘制词云。如：bg_pic = imread('读取一张图片.png')，背景图片的画布一定要设置为白色（#FFFFFF），然后显示的形状为不是白色的其他颜色。
                可以用ps工具将自己要显示的形状复制到一个纯白色的画布上再保存，就ok了。
            scale : float (default=1) //按照比例进行放大画布，如设置为1.5，则长和宽都是原来画布的1.5倍。
            min_font_size : int (default=4) //显示的最小的字体大小
            max_font_size : int or None (default=None) //显示的最大的字体大小
            max_words : number (default=200) //要显示的词的最大个数
            color_func : callable, default=None //生成新颜色的函数，如果为空，则使用 self.color_func
            relative_scaling : float (default=.5) //词频和字体大小的关联性

            regexp : string or None (optional) //使用正则表达式分隔输入的文本
            collocations : bool, default=True //是否包括两个词的搭配
            colormap : string or matplotlib colormap, default=”viridis” //给每个单词随机分配颜色，若指定color_func，则忽略该方法。

            width : int (default=400) //输出的画布宽度，默认为400像素
            height : int (default=200) //输出的画布高度，默认为200像素
            mode : string (default=”RGB”) //当参数为“RGBA”并且background_color不为空时，背景为透明。
            prefer_horizontal : float (default=0.90) //词语水平方向排版出现的频率，默认 0.9 （所以词语垂直方向排版出现频率为 0.1 ）
            font_step : int (default=1) //字体步长，如果步长大于1，会加快运算但是可能导致结果出现较大的误差。
            stopwords : set of strings or None //设置需要屏蔽的词，如果为空，则使用内置的STOPWORDS
        '''
    # wordcloud = WordCloud(background_color="white", max_words=20000, mask=bg_pic, max_font_size=60, random_state=42, scale=2, font_path="simhei.ttf").generate(text)
    # image_colors = ImageColorGenerator(bg_pic)
    # 显示词云图片
    # plt.imshow(wordcloud)
    '''
        off：关闭坐标轴
        equal：changes limits of x or y axis so that equal increments of x and y have the same length; a circle is circular.
        scaled
        tight
        image
        auto
        normal
        square
    '''
    plt.axis('off')
    plt.show()
    # 保存图片
    # wordcloud.to_file('test.jpg')


if __name__ == '__main__':
    itchat.login()  # 登录微信
    # get_friends_sex() # 获取男女比例
    get_data() # 获取微信好友数据
    # draw_wordcloud() # 制作词云
