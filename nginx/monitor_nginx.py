#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------------------
# 监控另外一台的nginx是否可以访问
# 如果有问题会发送邮件到指定邮箱
# ------------------------------------------------------------

import urllib2
import urlparse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


mail_host = "localhost"
mail_to_list = ["13918543465@139.com", "kevin.jiang@lexisnexis.com"]

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

def getNginxHeader(host):
    req = urllib2.Request(host)
    conn = urllib2.urlopen(req)
    conn.close()
    return conn


if __name__ == "__main__":
    rep = getNginxHeader('http://www.lexiscn.com')
    url = urlparse.urlparse(rep.url)
    if "hk.lexiscn.com" != url.netloc or 200 != rep.getcode():
        # 邮件内容
        mail_content = "Beijing server (Lexiscn) can not access"
        res = send_mail(mail_to_list, "Beijing server problem", mail_content)
