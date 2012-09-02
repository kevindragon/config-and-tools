#!/usr/bin/env python
# encoding=utf-8

import sys

if 2 > len(sys.argv):
    print 'please specify a name at least'
    sys.exit()

dbs = sys.argv[1:]

max_results = {"law": 700000, 
               "law_rows": 20505, 
               "case": 600000, 
               "caseCourt": 2000, 
               "ip_cases": 7000, 
               "hotnews": 8000, 
               "newlaw": 19000, 
               "profNewsletter": 2000, 
               "ip_hottopic": 6000, 
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
               "ep_news": 40000, 
               "ep_news_case": 4000, 
               "ep_news_law": 4500, 
               "overview": 2000, 
               "mini_book": 100, 
               "mini_bbs": 100, 
               "mini_book_chapter": 2000, 
               "ufida_qa": 0, 
               "company": 1000, 
               "deal": 400, 
               "topic_taxonomy": 3000, 
               "biz_news": 4500, 
               "law_news": 3000 }

url_prefix = "wget 'http://192.168.2.210:9002/action=query&anylanguage=true&printfields=id&databasematch={DBNAME}&text=*&maxresults={MAXRESULTS}' -O k{DBNAME}_210.xml"
url_prefix_2 = "wget 'http://192.168.2.211:9002/action=query&anylanguage=true&printfields=id&databasematch={DBNAME}&text=*&maxresults={MAXRESULTS}' -O k{DBNAME}_211.xml"

notexisteddb = []
for db in dbs:
    if db in max_results:
        tmpurl = url_prefix.replace("{DBNAME}", str(db))
        tmpurl = tmpurl.replace("{MAXRESULTS}", str(max_results[db]))
        print tmpurl
        tmpurl_2 = url_prefix_2.replace("{DBNAME}", str(db))
        tmpurl_2 = tmpurl_2.replace("{MAXRESULTS}", str(max_results[db]))
        print tmpurl_2
    else:
        notexisteddb.append(db)

# 生成SQL
dbconfig = {
    "law": "select tax.taxid from tax where tax.display=1", 
    "case": "select cases.case_id from cases where cases.display=1", 
    "journal": "select journal.article_id from (journal join journal_content on journal.article_id=journal_content.article_id) where journal.display_flag=1", 
    "pgl_content": "SELECT id  FROM ex_news WHERE sub_type=4 AND ipnews_category=1 AND FIND_IN_SET('1',alltype)  AND is_display=1", 
    "treaty": "select treaties.treaty_id from (treaties join treaties_content on treaties.treaty_id=treaties_content.treaty_id) where treaties.display=1", 
    "foreignlaw": "select foreign_law.law_id from (foreign_law join foreign_law_content on foreign_law.law_id=foreign_law_content.law_id) where foreign_law.display=1 ", 
    "expert": "select announceid from (listboard) where display=1 and listboard.root_id=0", 
    "ctax_topic": "select ctax_topic.news_id from (ctax_topic join ctax_topic_content on ctax_topic.news_id=ctax_topic_content.news_id) where ctax_topic.display=1", 
    "contract": "SELECT id FROM ex_news WHERE sub_type=4 AND ipnews_category=2 AND FIND_IN_SET('1',alltype)  AND is_display=1", 
    "hotnews": "select id from ex_news where sub_type=3 and ipnews_category=1 and find_in_set('1',alltype)  and is_display=1", 
    "newlaw": "select ex_news.id from ex_news where ex_news.sub_type=1 and find_in_set('1',alltype) and is_display=1", 
    "commentary": "select count(commentary.id) from commentary", 
    "profNewsletter": "select profNewsletter_Ext.id from (profNewsletter_Ext INNER JOIN profNewsletter ON profNewsletter_Ext.fk_profNewsletter_id =profNewsletter.id) where profNewsletter_Ext.isDisplay=1 AND profNewsletter_Ext.content is not null and profNewsletter_Ext.content<>''", 
    "ufida_qa": "select id from ex_expert_questions left join `user` on ex_expert_questions.user_id= `user`.userid where is_display=1 and `user`.username like 'ufida_%'", 
    "topic_taxonomy": "select id from ex_taxonomy", 
    "law_rows": "select law_rows.id from law_rows where is_display=1", 
    "ip_guide": "select ex_news.id from ex_news where ex_news.sub_type=4 and is_display=1", 
    "ip_hottopic": "select ex_news.id from ex_news where ex_news.sub_type=3 and ipnews_category = 1 and is_display=1 and alltype!='1' ", 
    "ip_news": "select ex_news.id from ex_news where ex_news.sub_type=1 and is_display=1 and find_in_set('2',alltype)", 
    "ex_questions": "select id from ex_expert_questions left join `user` on ex_expert_questions.user_id= `user`.userid where is_display=1 and `user`.username not like 'ufida_%'", 
    "ip_cases": "SELECT DISTINCT cases.case_id FROM cases JOIN ex_cases_taxonomy ON cases.case_id = ex_cases_taxonomy.case_id LEFT JOIN ex_taxonomy ON ex_cases_taxonomy.ex_taxonomy_id = ex_taxonomy.id WHERE display =1", 
    "ep_elearning": "SELECT ex_news.id FROM ex_news LEFT JOIN ex_news_files ON ex_news.id=ex_news_files.id WHERE  ex_news.sub_type=6 AND is_display=1 AND ex_news_files.ex_new_id IS NULL", 
    "ep_news": "SELECT ex_news.id FROM ex_news WHERE  ex_news.sub_type=1 AND is_display=1 AND ex_news.alltype<>'1'", 
    "ep_news_law": "SELECT ex_news.id FROM ex_news WHERE  ex_news.sub_type=3 AND is_display=1 AND ex_news.ipnews_category=2", 
    "ep_news_case": "SELECT ex_news.id FROM ex_news WHERE  ex_news.sub_type=3 AND is_display=1 AND ex_news.ipnews_category=3", 
    "overview": "select ex_news.id from ex_news where ex_news.sub_type=7 and is_display=1", 
    "mini_book": "select mod_book.id from mod_book where mod_book.display='Y'", 
    "mini_book_chapter": "select mod_category.id from mod_category left join mod_book on mod_category.bid=mod_book.id where mod_book.display='Y' and mod_category.display='Y'", 
    "mini_bbs": "select mod_bbs.id from mod_bbs where mod_bbs.display='Y' and mod_bbs.pid=0", 
    "caseCourt": "select caseCourt_Ext.id from (caseCourt_Ext INNER JOIN caseCourt ON caseCourt_Ext.fk_caseCourt_id = caseCourt.id) where caseCourt_Ext.isDisplay=1", 
    "company": "SELECT id FROM `ex_company` WHERE is_display=1", 
    "deal": "SELECT id FROM `ex_deal` WHERE is_display=1",
    "topic_taxonomy": "select id from ex_taxonomy", 
    "biz_news": "SELECT ex_news.id FROM ex_news WHERE  ex_news.sub_type=1 AND ipnews_category=2 AND is_display=1 AND ex_news.alltype<>'1' AND ex_news.alltype<>'2' AND ex_news.alltype<>'1,2' ", 
    "law_news": "SELECT ex_news.id FROM ex_news WHERE  ex_news.sub_type=1 AND ipnews_category=3 AND is_display=1 AND ex_news.alltype<>'1' AND ex_news.alltype<>'2' AND ex_news.alltype<>'1,2' ", 
    "newsletter": "select mnl_newsletters.nl_id from mnl_newsletters left join mnl_send_history on mnl_newsletters.nl_id=mnl_send_history.nl_id where mnl_newsletters.status='SENT' and mnl_newsletters.nl_id>=87 group by mnl_newsletters.nl_id;\nselect newsletter_ext.id from newsletter_ext where newsletter_ext.is_completed='Y' and newsletter_ext.is_sended='Y'"
}

print 
for db in dbs:
    if db in dbconfig:
        print db
        print dbconfig[db], "\n"

if len(notexisteddb):
    print ",".join(notexisteddb)
