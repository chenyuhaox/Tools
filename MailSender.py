import datetime as dt
import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from Setting import mail_info

def mail_sender(df,filepath,TotalFileNames,reportType):
    print('***开始发送邮件……***')
    receivers = mail_info['receivers']
    sender = mail_info['sender']
    mail_password = mail_info['mail_password']

    # 邮件标题内容
    mail_subject = '{}_{}点'.format(reportType,dt.datetime.now().strftime('%Y%m%d_%H'))

    df_filter=df[['title','substract','organ','reportDetailType','pdfLink']].copy()
    df_filter.to_csv(filepath + '/df_tmp.txt', sep='\t', index=False)
    lines = open(filepath + '/df_tmp.txt', "rb").readlines()
    mail_context=[]
    count=0
    for line in lines:
        count+=1
        if count==1:
            pass
        else:
            decode_line='{}.'.format(count-1)+line.decode('utf-8')
            reline=[l for l in decode_line.split() if l!=' ']
            join_reline='\n'.join(reline)
            mail_context.append(join_reline)
            mail_context.append(' ')
    mail_contexts='\n'.join(mail_context)
    os.remove(filepath + '/df_tmp.txt')

    msg = MIMEMultipart()
    msg["From"] = sender  # 发件人
    msg["To"] = ",".join(receivers)  # 收件人
    msg["Subject"] = mail_subject  # 邮件标题

    # 邮件正文
    msg.attach(MIMEText(mail_contexts,'plain', 'utf-8'))

    # 附件
    count=0
    for file in TotalFileNames:
        count+=1
        att = MIMEApplication(open(file, "rb").read())
        file_name=''.join(['{}.'.format(count)]+file.replace(filepath, '').split('_')[-1:])
        att.add_header('Content-Disposition', 'attachment', filename=file_name)
        msg.attach(att)

    try:
        smtpObj = smtplib.SMTP_SSL(mail_info['smtp'], 465)
        smtpObj.login(sender, mail_password)
        smtpObj.sendmail(sender, receivers, msg.as_string())
        print('***发送邮件成功！***')
        print('')
        smtpObj.quit()
    except smtplib.SMTPException as e:
        print('***发送邮件失败！***')
        print(e)


