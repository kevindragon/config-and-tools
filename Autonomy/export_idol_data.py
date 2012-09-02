#!/usr/bin/env python
# -*- coding=utf-8 -*-

import argparse
from autonomy import *
from autnparameter import *

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
                print url

                # 取id的正则表达式
                p = re.compile("\s*<%s>(\d+)</%s>" % ((printfields, )*2), 
                               re.IGNORECASE)

                edp = ExportDataPool(idol, url, p)
                edp.run()

    end_time = time.time()

    print "done total spent %s" % (end_time - start_time)

