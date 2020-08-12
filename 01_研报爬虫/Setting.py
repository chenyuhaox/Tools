import time

# 运行信息
work_info={
    'file_path': r'C:\Users\chenyuhao\Desktop\研报下载',
    'beginTime' : time.strftime('%Y-%m-%d', time.localtime()),
    'endTime' : time.strftime('%Y-%m-%d', time.localtime()),
    'reportType':['策略报告','宏观研究'],
    'substract_option':False
}
# 邮箱配置信息
mail_info = {
    'receivers' : ["xxxxx@qq.com",'xxxxx@163.com'], # 收件人
    'sender' : "xxxxx@126.com", # 发件人
    'mail_password' : "xxxxx", # smtp授权码
    'smtp':'smtp.126.com' #smtp地址
}

# 百度api配置信息(若substract_option=False，此处无需修改也可)
baidu_info = {
    'APP_ID' : 'xxxxx',
    'API_KEY' : 'xxxxx',
    'SECRET_KEY' : 'xxxxx'
}
