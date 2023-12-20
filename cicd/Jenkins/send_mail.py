from email.mime.text import MIMEText
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import smtplib
import os
import sys
from bs4 import BeautifulSoup

EMAIL_HOST_USER="platform@nullmax.ai"
EMAIL_HOST_PASSWORD="Nullmax@123!"

def modify_content():
    filename = "/home/lixialin/workspace/status.txt"
    text_map = {
        "0": "编译打包流程失败",
        "1": "推包失败",
        "2": "推包成功，回灌失败",
        "3": "回灌视频成功",
        "4": "评测成功"
    }
    if os.path.isfile(filename):
        print("status.txt 存在")
        with open(filename,'r') as f:
            status_code = f.readline(1)
        # os.system(f"rm {filename}")
    else:
        status_code = "0"
    content1 = text_map[status_code]
    if int(status_code) > 2:
        files = os.listdir("/home/lixialin/workspace/all_result")
        res_num = len(files)
        content1 = f"回灌了2个视频,成功了{res_num}个"
    if status_code == "4":
        content2 = "所有数据评测完成"
    else:
        content2 = "评测失败或未进入到评测流程"
    return content1,content2


receivers = ["chengjianlian@nullmax.ai","linaifan@nullmax.ai"]
## 建立server
server = smtplib.SMTP('smtp.partner.outlook.cn',587)
# 加密连线
server.starttls()
# 发送者的邮箱账号，密码
server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)

# 1、生成可放文字+图片的容器
msg=MIMEMultipart('related')
# 邮件主题
title = "【不要回复】邮件发送测试"
msg["Subject"] = title
# 发送者账号
msg["From"] = "DevOps"
# 接收者账号列表
msg['To'] = ",".join(receivers)

# 将评测结果作为附件

text_tuple = modify_content()

with open("test.html") as f:
    content = f.read()
    soup = BeautifulSoup(content,'html.parser')

con1 = soup.find(attrs={'name':'res1'})
con1.string = text_tuple[0]
con2 = soup.find(attrs={'name':'res2'})
con2.string = text_tuple[1]

msg.attach(MIMEText(str(soup),"html","utf-8"))

if "所有数据评测完成" == text_tuple[1]:
    att_f = MIMEText(open("/home/lixialin/workspace/data/eval_result/front_dist.xlsx","rb").read(),"base64","utf-8")
    att_f["Content-Type"] = "application/octest-stream"
    att_f["Content-Disposition"] = "attachment; filename=front_dist.xlsx"
    msg.attach(att_f)
# 发送者，接收者，发送的内容
server.sendmail(EMAIL_HOST_USER, receivers, msg.as_string())

#发送完关闭
server.close()
