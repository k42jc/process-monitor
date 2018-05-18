#coding:utf-8

"""
自动向指定邮箱发送邮件，标题为故障时间
"""
# -*- coding: utf-8 -*-

from email.header import Header
from email.mime.text import MIMEText
import smtplib
from config import Settings

def send(subject, content):
    try:
        sender = Settings['from_email'] # 发件人邮箱
        password = 'LJWtdmRz863j' # 发件人邮箱密码
        recipients = Settings['alarm_emails'] # 收件人邮箱
        host = 'smtpdm.aliyun.com' # 发件人邮箱主机
        port = 80

        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = sender
        msg['To'] = recipients
        msg['Subject'] = Header(subject, 'utf-8').encode()

        server = smtplib.SMTP(host, port)
        state = server.login(sender, password)
        if state[0] == 235:
            server.sendmail(sender, [recipients], msg.as_string())
            print "邮件发送成功"
        server.quit()
    except smtplib.SMTPException, e:
        print str(e)


# if __name__ == '__main__':
#     send()
