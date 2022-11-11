# -*- coding: UTF-8 -*-
"""
-------------------------------------------------
   FileName：        fti
   Description：     文字生成图片
   Author：          Kizai
   Date：            2022/11/8
-------------------------------------------------
"""
import os

from PIL import Image, ImageDraw, ImageFont  # 引入图片，画图笔，图片字体三个库
import textwrap  # 该库用于手动换行文字


# 获取文本最长行字符串的长度
def get_max_len_num(file_path: str):
    if os.path.exists(file_path):
        with open(file_path, "r", errors='ignore') as f:
            max_num = float("-inf")
            for lines in f.readlines():
                if len(lines) > max_num:
                    max_num = len(lines)
            return max_num
    else:
        print("file is not found!")


max_line = get_max_len_num("target.txt")
news_wrap = []  # 准备一个数组来装结果集
file = open("target.txt", 'r', errors='ignore')
news_content = file.readlines()
for line in news_content:  # 循环遍历数组中的每行文字，line是临时变量，指代当前所循环到的文字
    if len(line) < 4:  # 左边有四个空格， len(line)表示计算该行的字数，小于4个字的就舍弃
        continue  # 左边有八个空格，
    elif len(line) <= max_line:  # 若字数大于4个且小于29个 （限制每行字数不超过29字）
        news_wrap.append(line)  # 添加到数组中
    else:  # 若字数大于25个字
        wrap = textwrap.wrap(line, max_line)  # 按每行29个字分割成数组
        news_wrap = news_wrap + wrap  # 拼到结果数组中
print(news_wrap)  # 分割后的数组打印出来看看

IMG_SIZE = (max_line * 21, len(news_wrap) * 43)  # 图片尺寸 900x答案行数x每行行高
img = Image.new('RGB', IMG_SIZE, (255, 255, 255))  # 建一张新图，颜色用RGB，，底色三个255表示纯白
draw = ImageDraw.Draw(img)  # 创建一个画笔

header_position = (60, 30)  # 标题的横纵坐标位置
header_font = ImageFont.truetype('MiSans-Medium.ttf', 38)  # 标题的字体：小米字体，字号50
draw.multiline_text(header_position, '前端答案', '#ffbd39', header_font)  # 入参分别是坐标，文字内容，文字色号，文字字体

current_height = 100
for line in news_wrap:
    # if line.startswith('第'):
    #     news_font = ImageFont.truetype('MiSans-Medium.ttf', 40)  # 标题的字体楷体，字号50
    #     draw.text((60, current_height + 30), line, '#726053', news_font)
    #     current_height += 80
    # else:
    news_font = ImageFont.truetype('MiSans-Medium.ttf', 25)  # 内容字体30
    draw.text((60, current_height), line, '#3a0088', news_font)
    current_height += 40

img.show()  # 弹框展示图片
img.save('qianduan.png')  # 保存成文件

