from aip import AipOcr
import fitz
from fnmatch import fnmatchcase as match
import numpy as np
import re
import os
import string
from tqdm import tqdm
from Setting import baidu_info

def load_baidu_ocr():
    # --登陆百度，调用图片识别api--
    APP_ID = baidu_info['APP_ID']
    API_KEY = baidu_info['API_KEY']
    SECRET_KEY = baidu_info['SECRET_KEY']
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    return client

def pdf2graph(pdfPath, imagePath, zoom_x=8, zoom_y=8, rotate=int(0)):
    # --打开pdf--
    pdfDoc = fitz.open(pdfPath)
    # --将pdf拆分为图片保存--
    for pg in range(pdfDoc.pageCount):
        page = pdfDoc[pg]
        mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        pix = page.getPixmap(matrix=mat, alpha=False)
        pix.writePNG(imagePath + '/' + 'images_{}.png'.format(pg))
    return pdfDoc.pageCount

def text_process(page_words):
    raw_words = page_words.copy()
    # --计数标志--
    start_n = np.nan
    end_n = np.nan

    count = 0
    mark = True
    # --判断方式：（……图:……）和（……资料来源……）之间的文字识别结果往往为报告图片的内容--
    for n, words in enumerate(page_words):
        if match(words, '图*:*') or match(words, '图表*:*') :
            if mark:
                start_n = n - count
                mark = False
        elif match(words, '*来源*:*'):
            end_n = n - count
            if start_n < end_n:
                del raw_words[start_n:end_n + 1]
                count = count + end_n - start_n
                mark = True
                start_n = np.nan
                end_n = np.nan

    punctuation = string.punctuation
    count = 0
    raw_words_tmp = raw_words.copy()
    for n, words in enumerate(raw_words):
        if match(words, '*图*'):
            del raw_words_tmp[raw_words_tmp.index(words)]
        elif match(words, '*来源*'):
            del raw_words_tmp[raw_words_tmp.index(words)]
        elif match(words, '*证券*'):
            del raw_words_tmp[raw_words_tmp.index(words)]
        elif match(words, '*声明*'):
            del raw_words_tmp[raw_words_tmp.index(words)]
        elif match(words, '*免责*'):
            del raw_words_tmp[raw_words_tmp.index(words)]
        elif match(words, '*风险提示*'):
            del raw_words_tmp[raw_words_tmp.index(words)]
        elif match(words, '*专题*'):
            del raw_words_tmp[raw_words_tmp.index(words)]
        elif match(words, '*分析师*'):
            del raw_words_tmp[raw_words_tmp.index(words)]
        elif match(words, '*日期*'):
            del raw_words_tmp[raw_words_tmp.index(words)]
        elif match(words, '*报告*'):
            del raw_words_tmp[raw_words_tmp.index(words)]
        elif match(words, '*披露*'):
            del raw_words_tmp[raw_words_tmp.index(words)]
        elif re.match('^[0-9^a-z^A-Z]+$',re.sub(r'[{}]+'.format(punctuation),'',''.join([x for x in words if x!=' ']))):  # 只包含字母和数字
            del raw_words_tmp[raw_words_tmp.index(words)]
        elif words in punctuation:
            del raw_words_tmp[raw_words_tmp.index(words)]
        else:
            pass
    return raw_words_tmp

def graph2text(page_count,imagePath):
    # --删除含有以下关键词的页面--
    page_keywords=['*目录*','*……*','*评级*']
    texts=[]
    for page in tqdm(range(page_count)):
        # --按页循环，删除第一页和最后一页（主要针对研报）--
        if page==0 or page==page_count-1:
            os.remove(imagePath+'/images_{}.png'.format(page))
            pass
        else:
            page_words=[]
            # --图片文字识别--
            with open(imagePath+'/images_{}.png'.format(page), 'rb') as f:
                # --调用百度api识别图片文字--
                image = f.read()
                client=load_baidu_ocr()
                # --basicGeneral 50000图/天，basicAccurate 500图/天--
                text = client.basicGeneral(image) #高精度 basicAccurate

            # --识别文字提取--
            for word_dict in text["words_result"]:
                page_words.append(word_dict['words'])

            # --页面关键词判断--
            page_mark=True
            for key in page_keywords:
                if match(''.join(page_words),key):
                    page_mark=False

            if page_mark:
                # --单页识别结果处理--
                page_text=text_process(page_words)
                texts.append(''.join(page_text))
                os.remove(imagePath+'/images_{}.png'.format(page))
            else:
                os.remove(imagePath + '/images_{}.png'.format(page))

    return '，'.join(texts)

def pdf_extract(filepath,pdfPath):
    imagePath = filepath+'/PdfImg'
    pagecount = pdf2graph(pdfPath, imagePath)
    text=graph2text(pagecount, imagePath)

    return text