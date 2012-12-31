#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,urllib2,time
import xml.etree.ElementTree as ET

url = "http://192.168.2.211:9002/a=getstatus"

xml_res = urllib2.urlopen(url)
xml = xml_res.read()
root = ET.fromstring(xml)
rd = root.find("responsedata")
ds = rd.find("document_sections")

# 保存上一次的数据
tmpfile = "/tmp/document_sections_data_kj"
if not os.path.exists(tmpfile):
    open(tmpfile, "w").write("0")

last_count = open(tmpfile, "r").read()

open("autn_added_data.csv", "a").write("%s, %s\n" % (time.strftime("%Y-%m-%d %H"), (int(ds.text) - int(last_count))))

open(tmpfile, "w").write(ds.text)
