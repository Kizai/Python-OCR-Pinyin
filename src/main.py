# -*- coding: UTF-8 -*-
"""
-------------------------------------------------
   FileName：        main   
   Description：     Python识别中文文字并添加拼音返回
   Author：          Kizai
   Date：            2022/11/8
-------------------------------------------------
"""
import easyocr
from pypinyin import pinyin
import logging
from PIL import Image, ImageDraw, ImageFont  # 引入图片，画图笔，图片字体三个库
import textwrap  # 该库用于手动换行文字

# 日志设置
log_path = './run.log'
logging.basicConfig(filename=log_path, filemode='a', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(filename)s %(funcName)s %(lineno)d %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S")


# 获取OCR的识别结果
def get_ocr_results(picture_path: str):
    reader = easyocr.Reader(['ch_sim', 'en'], gpu=True)  # this needs to run only once to load the model into memory
    result_info = reader.readtext(picture_path)
    words = []
    for info in result_info:
        words.append(info[1])
    return words


# 把识别得到的文字转换成拼音
def convert_pinyin(content: str):
    res_pinyin = pinyin(content)
    py = []
    for single_pinyin in res_pinyin:
        py.append(str(single_pinyin).replace("['", '').replace("']", ''))
    return py


# 获取数组中最长的行长度
def get_list_max_line(text_list: list):
    if len(text_list):
        max_num = float("-inf")
        for text in text_list:
            if len(text) > max_num:
                max_num = len(text)
        return max_num
    else:
        logging.error("The list is null!")


if __name__ == '__main__':
    pic = {0: "png/chinese.png", 1: "png/shijing.png", 2: "png/smzjs.png"}
    res = []
    for i in range(0, len(pic)):
        ocr_res = get_ocr_results(pic[i])
        for word in ocr_res:
            word_pinyin = convert_pinyin(word)
            res_info = str(word_pinyin).replace("'", "").replace(",", "").replace('[', '').replace(']', '')
            res.append(res_info)
            res.append(word)
            print("{}\n{}".format(res_info, word))
            logging.info("{}\n{}".format(res_info, word))
    # print(res)
    max_line = get_list_max_line(res)
    news_wrap = []  # 准备一个数组来装结果集
    for line in res:  # 循环遍历数组中的每行文字，line是临时变量，指代当前所循环到的文字
        if len(line) < 1:  # 左边有四个空格， len(line)表示计算该行的字数，小于4个字的就舍弃
            continue  # 左边有八个空格，
        elif len(line) <= max_line:  # 若字数大于4个且小于29个 （限制每行字数不超过29字）
            news_wrap.append(line)  # 添加到数组中
        else:  # 若字数大于25个字
            wrap = textwrap.wrap(line, max_line)  # 按每行29个字分割成数组
            news_wrap = news_wrap + wrap  # 拼到结果数组中
    print(news_wrap)  # 分割后的数组打印出来看看

    IMG_SIZE = (max_line * 18, len(news_wrap) * 44)  # 图片尺寸 900x答案行数x每行行高
    img = Image.new('RGB', IMG_SIZE, (255, 255, 255))  # 建一张新图，颜色用RGB，，底色三个255表示纯白
    draw = ImageDraw.Draw(img)  # 创建一个画笔

    header_position = (60, 30)  # 标题的横纵坐标位置
    header_font = ImageFont.truetype('MiSans-Medium.ttf', 38)  # 标题的字体：小米字体，字号50
    draw.multiline_text(header_position, '图片识别转拼音结果：', '#ffbd39', header_font)  # 入参分别是坐标，文字内容，文字色号，文字字体

    current_height = 100
    for line in news_wrap:
        # if line.startswith('第'):
        #     news_font = ImageFont.truetype('MiSans-Medium.ttf', 40)  # 标题的字体楷体，字号50
        #     draw.text((60, current_height + 30), line, '#726053', news_font)
        #     current_height += 80
        # else:
        news_font = ImageFont.truetype('MiSans-Medium.ttf', 30)  # 内容字体30
        draw.text((60, current_height), line, '#3a0088', news_font)
        current_height += 40

    img.show()  # 弹框展示图片
    img.save('test.png')  # 保存成文件
