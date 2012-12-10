#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
监控IDOL的committed document slots是否达到上限
"""

import urllib2
import xml.etree.ElementTree as ET
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

ENVIROMENT = 'prd' # prd|alpha
ALERT_CEILING = 1900000

mail_host = "localhost"
mail_to_list = ["13918543465@139.com", "kevin.jiang@lexisnexis.com"]

if 'alpha' == ENVIROMENT:
    config = {
        'idol210': 'http://10.123.4.210:9002/action=getstatus',
        'idol211': 'http://10.123.4.210:9022/action=getstatus'
    }
elif 'prd' == ENVIROMENT:
    config = {
        'idol200': 'http://192.168.2.200:9002/action=getstatus',
        'idol210': 'http://192.168.2.210:9012/action=getstatus',
        'idol211': 'http://192.168.2.211:9002/action=getstatus'
    }
else:
    print 'please specify an ENVIROMENT'
    exit()

def send_mail(to, sub, content):
    me = "%s<%s>" % ('Kevin Jiang', 'kevin.jiang@lexisnexis.com')
    msg = MIMEMultipart('alternative')
    msg.attach(MIMEText(content.replace("\n", "<br>"), 'html'))
    msg['Subject'] = sub
    msg['From'] = "kevin.jiang@lexisnexis.com"
    msg['To'] = ";".join(to)
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.sendmail(me, to, str(msg))
        s.close()
        return True
    except Exception, e:
        return False
        

# 邮件内容
mail_content = "Hi Buddy\nSomething overflow\n\n"
overflow = False

for idol_name in config.keys():
    xml_res = urllib2.urlopen(config[idol_name])
    xml = xml_res.read()
    root = ET.fromstring(xml)
    rd = root.find('responsedata')
    cd = rd.find('committed_documents')
    # 如果超过报警上限，组织邮件内容
    if cd.text >= ALERT_CEILING:
        if not overflow:
            overflow = True
        mail_content += "%s's committed documents is overflow\n" % idol_name
        mail_content += "%s: <font color='red'>%s</font>\n\n" % (idol_name, cd.text)

if overflow:
    res = send_mail(mail_to_list, "commited documents overflow", mail_content)
    if not res:
        print 'sent failed'

