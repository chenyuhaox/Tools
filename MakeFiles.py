import xlwt
import os
import pandas as pd
from fnmatch import fnmatchcase as match

def CreateFiles(file_path, reportType,substract_option):
    print('***检查下载记录***')
    dirs = os.listdir(file_path)
    type = reportType

    # --创建存储pdf转换拆分图片的文件夹--
    if substract_option:
        if 'PdfImg' in dirs:
            pass
        else:
            os.makedirs(file_path + '/PdfImg/')

    # --创建保存下载记录的Excel文件--
    if 'DownloadRecords.xls' in dirs:
        DownloadRecords = pd.read_excel(file_path + '/DownloadRecords.xls')
    else:
        xls = xlwt.Workbook()
        sht1 = xls.add_sheet('DownloadRecords')
        sht1.write(0, 0, 'title')
        sht1.write(0, 1, 'substract')
        sht1.write(0, 2, 'pdate')
        sht1.write(0, 3, 'author')
        sht1.write(0, 4, 'organ')
        sht1.write(0, 5, 'reportType')
        sht1.write(0, 6, 'pdfLink')
        xls.save(file_path + '/DownloadRecords.xls')
        DownloadRecords = pd.read_excel(file_path + '/DownloadRecords.xls')

    # --创建一级文件夹--
    if type in dirs:
        pass
    else:
        os.makedirs(file_path + '/{}/'.format(type))

    # --创建二/三级文件夹--
    if type == '策略报告':
        second_types = ['深度专题', '观察点评', '科创板', '海外']
        third_types = ['日报', '周报', '月报', '季报年报', '金股']
    else:
        second_types = ['深度专题', '观察点评', '海外']
        third_types = ['日报', '周报', '月报', '季报年报']

    # --创建二级文件夹--
    if '定期报告' in os.listdir(file_path + '/{}/'.format(type)):
        pass
    else:
        os.makedirs(file_path + '/{}/定期报告/'.format(type))

    for second_type in second_types:
        if second_type in os.listdir(file_path + '/{}/'.format(type)):
            pass
        else:
            os.makedirs(file_path + '/{}/{}/'.format(type, second_type))
    # --创建三级文件夹（../定期报告/)--
    for third_type in third_types:
        if third_type in os.listdir(file_path + '/{}/定期报告/'.format(type)):
            pass
        else:
            os.makedirs(file_path + '/{}/定期报告/{}/'.format(type, third_type))

    return DownloadRecords

def ClassifyReportType(name):
    type_dict={'定期报告/金股':['*金股*'],
               '科创板': ['*科创*'],
               '海外':['*全球*','*海外*','*出海*','*外围*','*国外*','*境外*'],
               '观察点评':['*评*','*解读*','*观点*','*前瞻*','*热点*','*观察*'],
               '定期报告/日报':['*收盘*','*午盘*','*日报*','*早报*','*盘前*','*早知道*','*解盘*','*每日*','*日监控*','*日观察*','*盛视聚焦*','*联储视点*','*市场点睛*','*A股市场观察*','*复利防御*','*速递*','*让中泰策略告诉你*'],
               '定期报告/周报':['*周*','专刊','A股资金追踪','股市资金跟踪','海外市场观察','全球资金流向监测'],
               '定期报告/月报':['*半月*','*月报*','*月度*','*月观点*','*每月*','*月刊*','*月监控*','*月观察*','*一月点评*','*年*月*','*月资产配置*'],
               '定期报告/季报年报':['*半年*','*中期*','*Q1*','*Q2*','*Q3*','*Q4*','*季度*','*年度*'],
               '深度专题': ['*深度*', '*专题*', '*系列*', '*杂谈*', '*复盘*']
               }
    for key,value in type_dict.items():
        for keyword in value:
            if match(name, keyword):
                return key
    return '未分类'
