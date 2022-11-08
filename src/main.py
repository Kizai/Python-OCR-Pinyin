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


if __name__ == '__main__':
    pic = {0: "png/chinese.png", 1: "png/shijing.png"}
    for i in range(0, len(pic)):
        ocr_res = get_ocr_results(pic[i])
        for word in ocr_res:
            word_pinyin = convert_pinyin(word)
            res_info = str(word_pinyin).replace("'", "").replace(",", "").replace('[', '').replace(']', '')
            print("{}\n{}".format(res_info, word))
            logging.info("{}\n{}".format(res_info, word))
