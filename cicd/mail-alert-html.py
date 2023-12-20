#!/usr/bin/python
#-*- encoding:utf-8 -*-
import os
import sys
import smtplib,mimetypes
#from email import Encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

kk=sys.argv[1]
ll=sys.argv[2]
hh=sys.argv[3]
pipe=os.popen(ll).read()
msg = MIMEMultipart()
msg['Subject'] = str(kk)
msg['From'] = 'yangchentao@nullmax.ai'
msg['To'] =hh
#msg_str = 'this is a test email sending by python'
#txt = MIMEText(msg_str, 'plain', 'utf-8')
txt = MIMEText(str(pipe),_charset='utf-8')
txt=MIMEText(str(pipe),"html","utf-8")
msg.attach(txt)
s = smtplib.SMTP('smtp.partner.outlook.cn',587)
s.starttls()
s.login('yangchentao@nullmax.ai','nullmax@123')
s.sendmail('yangchentao@nullmax.ai',hh,msg)
s.close()