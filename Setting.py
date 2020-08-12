import time

# 运行信息
work_info={
    'file_path': '//Mac/Home/Desktop/report',
    'beginTime' : time.strftime('%Y-%m-%d', time.localtime()),
    'endTime' : time.strftime('%Y-%m-%d', time.localtime()),
    'reportType':['策略报告','宏观研究'],
    'substract_option':False
}
# 邮箱配置信息
mail_info = {
    'receivers' : ["yhaochen@qq.com",'chenyuhao_mail@163.com'], # 收件人
    'sender' : "report_sender@126.com", # 发件人
    'mail_password' : "OELOQYISRRKJGIAY", # smtp授权码
    'smtp':'smtp.126.com' #smtp地址
}

# 百度api配置信息
baidu_info = {
    'APP_ID' : '21864967',
    'API_KEY' : '55c7jFW9xDdexNtIaPvLZQOE',
    'SECRET_KEY' : 'mbRjQwj6b4whliWduGN8C4HB7RGEj7Gj'
}
