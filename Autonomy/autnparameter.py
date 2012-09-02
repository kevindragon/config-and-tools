#!/usr/bin/env python
# -*- coding=utf-8 -*-

import config

def get_url_pattern(idol, autndb):
    urltemplate = ('/action=query&anylanguage=true&text=*&'
                   'databasematch=%s&maxresults=%d&printfields=%s')

    urls = {}
    for db in autndb:
        printfields = "ID"
        if "hotnews" == db:
            printfields = "ARTICLE_ID"
            
        maxresults = config.total_resuls[db]
        url = urltemplate % (db, maxresults, printfields)
        urls[db] = {}
        for i in idol:
            urls[db][i] = config.IDOL_HOST_DICT[i]+url

        if config.SQL_LIST.has_key(db):
            urls[db]['sql'] = config.SQL_LIST[db]

    return urls

