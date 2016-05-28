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

  1463788802:172.17.21.55:'HTTP/1.1 200 OK  ST\:upnp\:rootdevice  EXT\:  (... rest of line ...)
    |          |
    |          .---> IP
    .---> timestamp (UTC) epoch

"""


count_unparseable=0
count_parseable=0
reader = csv.reader(sys.stdin, delimiter=':', quotechar="'")
for line in reader:
    ts=float(line[0])
    # postgresql format: 2016-05-08 02:00:04.126444+02
    ts = time.strftime("%Y-%m-%d %H:%M:%S.0+00", time.localtime(ts))     # remember, we are UTC 
    ip = line[1]
    try:
        print("'{ts}'{sep}{risk}{sep}'{ip}'".format(sep=sep,risk=5,ts=ts,ip=ip))
        count_parseable+=1
    except Exception as e:
        print(type(e), file=sys.stderr)    # the exception instance
        print(e.args, file=sys.stderr)     # arguments stored in .args
        print(e, file=sys.stderr) 
        print("could not parse '{}'".format(line), file=sys.stderr) 
        count_unparseable+=1


print("parseable lines: {}".format(count_parseable), file=sys.stderr)
print("unparseable lines: {}".format(count_unparseable), file=sys.stderr)

