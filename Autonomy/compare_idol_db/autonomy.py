#!/usr/bin/env python
# -*- coding=utf-8 -*-

__doc__ = """\
定义一些跟IDOL相关的类。

比如去IDOL里面取数据，使用多线程取一个仓库里面的数据。
"""

import urlparse, urllib2, threading, time, os, re
from autnparameter import *

class ExportDataPool(object):
    def __init__(self, idol, url, p):
        self.idol = idol
        self.url = url
        self.p = p
    
    def run(self):
        url_components = urlparse.urlparse(self.url)        
        query_strs = urlparse.parse_qs(url_components.path)
        db_name = query_strs['databasematch'][0]

        # 计算线程的数量,取maxresults,如果超过10000，就使用多线程取数据
        max_results = int(query_strs['maxresults'][0])
        if max_results > 100000:
            thread_num = 4
        elif 50000 < max_results < 100000:
            thread_num = 2
        else:
            thread_num = 1

        # 每个请求的请求数据量
        each_results = int(max_results/thread_num)
        urls, resfiles = [], []

        # 拼装每一个请求的url
        for x in range(thread_num):
            start = x * each_results + 1
            max_res = (x+1) * each_results
            if (x+1) == thread_num and max_res < max_results:
                max_res = max_results
                
            query_strs['start'] = [str(start)]
            query_strs['maxresults'] = [str(max_res)]
            qs = sorted([k+"="+query_strs[k][0] for k in query_strs.iterkeys()])
            urls.append(urlparse.urljoin(self.url, "&".join(qs)))
            if thread_num == 1:
                tmpresfile = self.idol+"-"+query_strs["databasematch"][0]+".xml"
            else:
                tmpresfile = (self.idol + "-" +
                              query_strs["databasematch"][0] +
                              "-" + str(x) + ".xml")
            resfiles.append(tmpresfile)
        
        print "there are %d threads will to run" % thread_num

        threads = []
        for i in range(thread_num):
            threads.append(GetData(urls[i], resfiles[i]))
            
        for t in threads:
            t.start()
            print "thread %s start \n%s" % (t, t.url+" "+t.sfile)

        [t.join() for t in threads]
            
        print "all threads are completed\nstart format and pick up id from xml file"

        # 格式化xml，取id保存到文件
        idfiles = []
        for f in resfiles:
            print "xmllint --format %s" % f
            tmpout = os.popen("xmllint --format %s" % f).read()
            fp = open(f, "w")
            fp.write(tmpout)
            fp.close()
            
            idsfn = os.path.splitext(f)[0] + ".ids"
            idfiles.append(idsfn)
            ids_content = self.pick_id(tmpout.split("\n"), self.p)
            fp = open(idsfn, "w")
            fp.write("\n".join(ids_content)+"\n")
            fp.close()
            
        combine_cmd = ("cat %s > %s-%s.ids" %
                        (" ".join(idfiles), self.idol, db_name))
        print combine_cmd
        thread_num > 1 and os.system(combine_cmd)
            
        print "pick up done"

    def pick_id(self, lines, p):
        ids = []
        for l in lines: 
            m = p.match(l)
            if m is not None:
                ids.append(m.groups()[0])
        return ids

# 取数据的线程类
class GetData(threading.Thread):
    def __init__(self, url, sfile):
        threading.Thread.__init__(self)
        self.url = url
        self.sfile = sfile

    def run(self):
        opener = urllib2.build_opener()
        r = urllib2.Request(self.url)
        fop = opener.open(r)
        data = fop.read()
        f = open(self.sfile, "w")
        f.write(data)
        f.close()
        fop.close()

