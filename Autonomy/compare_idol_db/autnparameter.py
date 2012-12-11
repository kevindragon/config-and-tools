#!/usr/bin/env python
# -*- coding=utf-8 -*-

import config


def get_url_pattern(idol, autndb):
    """获取指定idol里面单独一个仓库的查询命令

    Args:
        idol: 指定是哪一个idol
        autndb: 指定查询哪一个库

    Returns:
        a query statement for specify idol and database
    """
    urltemplate = ('/action=query&anylanguage=true&combine=simple&text=*&'
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
        """
        if config.SQL_LIST.has_key(db):
            urls[db]['sql'] = config.SQL_LIST[db]
        """
    return urls


