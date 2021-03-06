#!/usr/bin/env python
# -*- coding=utf-8 -*-

import argparse
from autonomy import *
from autnparameter import *
from database import *

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Export data from IDOL you sepcify.')
    parser.add_argument("-id", dest="idoldblist", 
                        help="idol,dblist[-idol,dblist]")
    args = parser.parse_args()

    if None == args.idoldblist:
        parser.print_help()
        exit()

    idoldblist = [v.split(',') for v in args.idoldblist.split('-')]
    print idoldblist

    start_time = time.time()

    for idoldb in idoldblist:
        idols = (idoldb[0], )
        autndbs = tuple(idoldb[1:])

        urls = get_url_pattern(idols, autndbs)

        for db in autndbs:
            for idol in idols:
                printfields = 'id'
                if 'hotnews' == db:
                    printfields = 'article_id'
                url = urls[db][idol]

                # 取id的正则表达式
                p = re.compile("\s*<%s>(\d+)</%s>" % ((printfields, )*2), 
                               re.IGNORECASE)

                edp = ExportDataPool(idol, url, p)
                edp.run()

    # print sql statement
    dbs_name = []
    dbs_name = {}.fromkeys(reduce(lambda x,y: x+y[1:], idoldblist, dbs_name)).keys()
    gdfd = GetDataFromDatabase(dbs_name)
    allsql = gdfd.get_all_sql()
    for dbsql in allsql.keys():
        print "%s:\n%s" % (dbsql, allsql[dbsql])

    data_in_db = gdfd.get_data()
    for db,ids in data_in_db.items():
        filep = open("%s.csv" % db, "w")
        print >> filep, "\n".join(map(str, ids))
    end_time = time.time()

    print "done total spent %s" % (end_time - start_time)

