import math, random
import requests, json, re, time
import urllib
from urllib.request import urlretrieve
from lxml import etree
from FastTextRank4Sentence import *
import logging
from MailSender import *
from MakeFiles import *
from PdfProcess import *
import sys

logging.propagate = False
logging.getLogger().setLevel(logging.ERROR)

User_Agent_List = [
    # Opera
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
    "Opera/8.0 (Windows NT 5.1; U; en)",
    "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
    # Firefox
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    # Safari
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
    # chrome
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
    # 360
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    # 淘宝浏览器
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    # 猎豹浏览器
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    # QQ浏览器
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    # sogou浏览器
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
    # maxthon浏览器
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
    # UC浏览器
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",
]
headers = {
    'Referer': 'http://data.eastmoney.com/report/macresearch.jshtml',
    'User-Agent': random.choice(User_Agent_List),
}

def get_total_page(url, headers):
    response = requests.get(url, headers=headers)
    rsp = re.search(r'{.*\}', response.text)
    reportcounts = json.loads(rsp.group()).get("hits")
    pagesize = json.loads(rsp.group()).get("size")
    if pagesize==0:
        print('***无数据***')
        sys.exit(0)
    else:
        if reportcounts / pagesize == 1:
            pages = math.floor(reportcounts / pagesize)
        else:
            pages = math.floor(reportcounts / pagesize) + 1
    return pages, reportcounts

def parse_url(url, headers, reportType, DownloadRecords, FilePath,hits,substract_option,report_counts=0):
    response = requests.get(url, headers=headers)
    rsp = re.search(r'{.*\}', response.text)
    datas = json.loads(rsp.group()).get("data")
    items = []
    FileNames=[]
    for data in datas:
        report_counts+=1
        item = {'title': '','substract':'', 'pdate': '', 'author': '', 'organ': '', 'reportType': '', 'reportDetailType': '', 'pdfLink': ''}
        # --报告题目--
        title= data.get("title")
        # --替换题目中的特殊字符--
        for punc in [':','/','&',' ']:
            title = title.replace(punc, '')
        item["title"]=title
        # --发布日期（平台上传更新的日期，与实际发布日期可能略有出入）--
        item["pdate"] = data.get("publishDate", "").split(" ")[0]
        # --报告作者--
        item["author"] = data.get("researcher", "")
        # --报告发布公司--
        item["organ"] = data.get("orgSName", "")
        # --报告类型（策略报告/宏观研究）——
        item["reportType"] = reportType
        # --报告细分类别（根据报告名称粗分）--
        reportDetailType=ClassifyReportType(item["title"])
        item["reportDetailType"] = reportDetailType

        # --打印下载进度--
        print('')
        print('***正在下载第{}篇/共{}篇 @{}***'.format(report_counts, len(datas), dt.datetime.now()))
        print('报告信息：{}-{}-{}-{}'.format(item["organ"],item["reportDetailType"],item["title"],item["pdate"]))

        encodeUrl = data.get("encodeUrl", "")
        # --根据Excel中保存的下载记录判断是否重复下载--
        if (item["title"] in DownloadRecords.title.tolist()) & (item["pdate"] in DownloadRecords.pdate.tolist()):
            print('重复下载!')
        else:
            if item['reportType'] == '策略报告':
                # --下载报告文件--
                detail_url = "http://data.eastmoney.com/report/zw_strategy.jshtml?encodeUrl={}".format(encodeUrl)
                request = requests.get(detail_url, headers=headers)
                item['pdfLink'],FileName,FormatType= download_pdf(request, item, FilePath,reportDetailType)
                print('下载成功!')
                # --生成文本摘要--
                if substract_option:
                    item['substract'] = MakeSubsrtact(FilePath, FileName, FormatType)
            else: # item['reportType'] == '宏观研究':
                # --下载报告文件--
                detail_url = "http://data.eastmoney.com/report/zw_macresearch.jshtml?encodeUrl={}".format(encodeUrl)
                request=requests.get(detail_url, headers=headers)
                item['pdfLink'],FileName,FormatType= download_pdf(request, item, FilePath,reportDetailType)
                print('下载成功!')
                # --生成文本摘要--
                if substract_option:
                    item['substract']=MakeSubsrtact(FilePath,FileName,FormatType)

            FileNames.append(FileName)
            items.append(item)
    df = pd.DataFrame(items)
    return df,FileNames

def MakeSubsrtact(FilePath,FileName,FormatType):
    print('开始提取摘要……')
    substract=''
    if FormatType == 'pdf':
        try:
            text = pdf_extract(FilePath, FileName)
            substract_fun = FastTextRank4Sentence(use_w2v=False, tol=0.0005)
            substract_text = substract_fun.summarize(text)
            substract = '\n'.join(substract_text)
            print('成功提取摘要！')
        except:
            print('提取摘要失败！')
    else:
        print('提取摘要失败，由于格式非PDF！')
    return substract

def download_pdf(response, item, filepath,reportDetailType):
    date = dt.datetime.strptime(item['pdate'], '%Y-%m-%d').strftime('%Y%m%d')
    html = etree.HTML(response.text)
    # --提取报告下载链接--
    FileLink= html.xpath('.//span[@class="to-link"]/a[@class="pdf-link"]/@href')[0]
    # --识别报告格式--
    FileFormats=['pdf','xlsx','xls','png','jpeg','csv','doc','docx']
    FormatType='pdf'
    for FileFormat in FileFormats:
        if FileFormat in FileLink[-5:]:
            FormatType=FileFormat
    # --生成报告存储路径和报告存储名--
    if reportDetailType=='未分类':
        FileName = filepath + '/' + item['reportType'] + '/' + date + '_' + item["organ"] + '_' + item["title"] + '.{}'.format(FormatType)
    else:
        FileName = filepath + '/' + item['reportType'] +'/'+reportDetailType+ '/' + date + '_' + item["organ"] + '_' + item["title"] + '.{}'.format(FormatType)
    # --下载报告文件--
    try:
        print('开始下载报告，格式为{}……'.format(FormatType))
        urllib.request.urlretrieve(FileLink, FileName)
    except:
        print('无法下载！')
        print(FileLink)

    return FileLink,FileName,FormatType

def DownloadReport(reportType, beginTime, endTime, filepath,substract_option):
    # --初始链接--
    startUrl = "http://reportapi.eastmoney.com/report/jg?cb={cb}&pageSize=100&beginTime={begin}&endTime={end}&pageNo={page}&fields=&qType={type}&orgCode=&author=&_={timestamp}"
    codeType = {"策略报告": "datatable7270063", "宏观研究": "datatable1062280"}
    typestr = {"策略报告": str(2), "宏观研究": str(3)}
    timestamp = round(time.time() * 1000)

    # --获取页数和报告数--
    url = startUrl.format(cb=codeType[reportType], begin=beginTime, end=endTime, page=1, type=typestr[reportType], timestamp=timestamp)
    pages, reportcounts = get_total_page(url, headers)

    # --生成保存路径--
    DownloadRecords = CreateFiles(filepath,reportType,substract_option)

    # --开始下载报告--
    print('***开始下载 {}***'.format(reportType))

    records=pd.DataFrame()
    TotalFileNames=[]
    for page in range(0, pages):
        # --按页循环，增加延时--
        sleeptime=random.randint(0,10)
        time.sleep(sleeptime)
        # --生成链接--
        timestamp = round(time.time() * 1000)
        url = startUrl.format(cb=codeType[reportType], begin=beginTime, end=endTime, page=page,type=typestr[reportType], timestamp=timestamp)
        # --提取页面数据--
        df,FileNames = parse_url(url, headers, reportType, DownloadRecords, filepath,reportcounts,substract_option)

        TotalFileNames=TotalFileNames+FileNames
        records= pd.concat([records, df], axis=0)

        # --下载记录保存--
        if pages>3:
            DownloadRecords = pd.concat([DownloadRecords, df], axis=0)
            DownloadRecords.to_excel(filepath + '/DownloadRecords.xls', encoding='gbk', index=False)
        else:
            DownloadRecords = pd.concat([DownloadRecords, records], axis=0)
            DownloadRecords.to_excel(filepath + '/DownloadRecords.xls', encoding='gbk', index=False)
        print('')
    try:
        # --打印本次下载结果--
        record_summary=records['reportDetailType'].value_counts()
        print('***{} 下载结果***'.format(reportType))
        print(record_summary)
        print('')
        # --邮件发送结果--
        mail_sender(records,filepath,TotalFileNames,reportType)
    except:
        print('全部重复下载')
