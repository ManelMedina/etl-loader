#!/usr/bin/env python

from __future__ import print_function

import sys
import argparse
import fileinput

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', action='store_true', help="turn on verbose mode.")
parser.add_argument('-n', '--rate',    type=int, help='Sample rate')

args = parser.parse_args()
if args.rate:
        rate=args.rate
else:
        rate=-1

i=0
for line in sys.stdin:
    if (rate > 0):
        if (not (i % rate)):
            print(line, end='')
    else:
        print(line, end='')     # if no sample rate given, print everything

    i+=1
