#!/usr/bin/env python

from __future__ import print_function
import sys
import argparse
import csv
import time

debug=False
sep=','

# input file format:
"""
# format:
#  IP1:53:64.21.0.0:NULL:1367107201.262564:0:0:0
#      |  |         |    |                 | | |-> 7, correct
#      |  |         |    |                 | .--> 6, ra
#      |  |         |    |                 .--> 5, rcode
#      |  |         |    .---> 4, timestamp (UTC, epoch)
#      |  |         .----> 3, secondary IP
#      |  .---> 2, primary IP
#      .------> 1, port

"""


count_unparseable=0
count_parseable=0
reader = csv.reader(sys.stdin, delimiter=':', quotechar="'")
for line in reader:
    ts=float(line[4])
    # postgresql format: 2016-05-08 02:00:04.126444+02
    ts = time.strftime("%Y-%m-%d %H:%M:%S.0+00", time.localtime(ts))     # remember, we are UTC 
    ip = line[2]
    try:
        print("'{ts}'{sep}{risk}{sep}'{ip}'".format(sep=sep,risk=1,ts=ts,ip=ip))
        count_parseable+=1
    except Exception as e:
        print(type(e), file=sys.stderr)    # the exception instance
        print(e.args, file=sys.stderr)     # arguments stored in .args
        print(e, file=sys.stderr) 
        print("could not parse '{}'".format(line), file=sys.stderr) 
        count_unparseable+=1


print("parseable lines: {}".format(count_parseable), file=sys.stderr)
print("unparseable lines: {}".format(count_unparseable), file=sys.stderr)

