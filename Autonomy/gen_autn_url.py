#!/usr/bin/env python
# encoding=utf-8

import sys

if 2 > len(sys.argv):
    print 'please specify a name at least'
    sys.exit()

dbs = sys.argv[1:]

max_results = {"law": 608466, 
               "law_rows": 20505, 
               "case": 500000, 
               "caseCourt": 2000, 
               "ip_cases": 7000, 
               "hotnews": 7000, 
               "newlaw": 10000, 
               "profNewsletter": 2000, 
               "ip_hottopic": 5000, 
               "ex_questions": 3000, 
               "dtt": 1000, 
               "journal": 1000, 
               "contract": 2000, 
               "expert": 5000, 
               "ip_news": 4900, 
               "ip_guide": 7000, 
               "treaty": 5000, 
               "foreignlaw": 100, 
               "pgl_content": 700, 
               "commentary": 100, 
               "ep_elearning": 200, 
               "ep_news": 30000, 
               "ep_news_case": 3000, 
               "ep_news_law": 4500, 
               "overview": 1500, 
               "mini_book": 100, 
               "mini_bbs": 100, 
               "mini_book_chapter": 2000, 
               "ufida_qa": 0, 
               "company": 600, 
               "deal": 400, 
               "topic_taxonomy": 3000, 
               "biz_news": 3500, 
               "law_news": 3000 }

url_prefix = "http://192.168.2.200:9003/action=query&combine=simple&anylanguage=true&printfields=id&Output=File&databasematch={DBNAME}&FileName=k{DBNAME}.xml&OutputEncoding=UTF8&text=*&maxresults={MAXRESULTS}"

notexisteddb = []
for db in dbs:
    if db in max_results:
        tmpurl = url_prefix.replace("{DBNAME}", str(db))
        tmpurl = tmpurl.replace("{MAXRESULTS}", str(max_results[db]))
        print tmpurl
    else:
        notexisteddb.append(db)

if len(notexisteddb):
    print ",".join(notexisteddb)
