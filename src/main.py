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

# 日志设置
log_path = './run.log'
logging.basicConfig(filename=log_path, filemode='a', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(filename)s %(funcName)s %(lineno)d %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S")


# 获取OCR的识别结果
def get_ocr_results(picture_path: str):
    reader = easyocr.Reader(['ch_sim', 'en'])  # this needs to run only once to load the model into memory
    result = reader.readtext(picture_path)
    return result


# 把识别得到的文字转换成拼音
def convert_pinyin(content: str):
    res_pinyin = pinyin(content)
    py = []
    for single_pinyin in res_pinyin:
        py.append(str(single_pinyin).replace("['", '').replace("']", ''))
    return py


if __name__ == '__main__':
    pic = "png/chinese.png"
    res = get_ocr_results(pic)
    # print(res)
    print(convert_pinyin(res), res)
    print(convert_pinyin("人民就是江山，江山就是人民，中国共产党打江山！"))
