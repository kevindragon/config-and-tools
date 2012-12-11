#/usr/bin/env python
# encoding=utf-8

import re, sys

if len(sys.argv) < 2:
    print "\nplease specify a filename\n"
    print "Usage:\npickupid.py filename\n"
    exit()

filename = sys.argv[1]

#p = re.compile("\s*<ID>(\d+)</ID>", re.IGNORECASE)
p = re.compile("\s*<ID>(\d+)</ID>", re.IGNORECASE)

fp = open(filename)
for l in fp:
    m = p.match(l)
    if m is not None:
        print m.groups()[0]

fp.close()


