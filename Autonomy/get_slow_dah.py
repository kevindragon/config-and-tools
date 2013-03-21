#!/usr/bin/env python
# -*- coding: utf-8 -*-

__doc__ = """获取IDOL日志里面比较慢的请求"""

import sys
import re

filename = sys.argv[1]

#read file content
logs = [ x.strip() for x in open(filename, "r").readlines()]

p = re.compile("\[(\d)\]\s*Engine \d returned in ([0-9.]+) ([^.]+)")
x = 0
slow_logs = []
for n, line in enumerate(logs):
    matched = p.findall(line)
    if len(matched):
        if "seconds"==matched[0][2] and float(matched[0][1]) > 2:
            tmp_slow = matched[0][1]
            point = n-1
            while point > 0:
                if re.search("\d\d \["+matched[0][0]+"\] action=", logs[point], re.IGNORECASE):
                    tmp_slow = (float(tmp_slow), logs[point][24:logs[point].rfind(' ')])
                    break
                point -= 1
            slow_logs.append(tmp_slow)

slow_log_sorted = sorted(slow_logs, lambda x,y: cmp(y[0], x[0]))

print "\n".join(map(lambda x: str(x[0])+"; "+x[1], slow_log_sorted))
