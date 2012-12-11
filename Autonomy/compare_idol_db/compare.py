#!/usr/bin/env python
# encoding=utf-8

import sys, os, time

if 3 > len(sys.argv):
    print """
please specify two files

Usage:
    compare.py filename1 filename2
    """
    sys.exit()

t1 = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

file1 = sys.argv[1]
file2 = sys.argv[2]

if not os.path.exists(file1):
    print "file %s not exists" % file1
if not os.path.exists(file2):
    print "file %s not exists" % file1

list1 = frozenset([x.strip("\n") for x in open(file1)])
list2 = frozenset([x.strip("\n") for x in open(file2)])

t2 = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

subtraction_db_autn = list1 - list2
subtraction_autn_db = list2 - list1

t3 = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

print "\n", len(list1), len(list2)
print "-"*10, "f - s = ", len(subtraction_db_autn), "-"*10, "\n", ",".join(subtraction_db_autn)
print "\n"
print "-"*10, "s - f = ", len(subtraction_autn_db), "-"*10, "\n", ",".join(subtraction_autn_db)
print "\n%s\n%s\n%s" % (t1, t2, t3)

