#!/usr/bin/python
from __future__ import print_function
import fileinput
import radix
import sys
import argparse
import csv
import geoip2.database


sep=":"
verbose = False
col=7


parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose',   action='store_true', help="turn on verbose mode.")
parser.add_argument('-s', '--separator', type=str, default=sep, help='CSV file field separator.')

args = parser.parse_args()

if args.verbose:
    verbose = True
if args.separator:
    sep = args.separator

infile = sys.stdin

#
# parse main file
#
i=0
count_filtered=0
count_passed=0
csvreader = csv.reader(infile, delimiter=sep, quotechar="'")
csvwriter = csv.writer(sys.stdout, delimiter=sep, quotechar="'") #, quoting=csv.QUOTE_MINIMAL)

# format:
#  IP1:53:64.21.0.0:NULL:1367107201.262564:0:0:0
#      |  |         |    |                 | | |-> correct
#      |  |         |    |                 | .--> ra
#      |  |         |    |                 .--> rcode
#      |  |         |    .---> timestamp (UTC, epoch)
#      |  |         .----> secondary IP
#      |  .---> primary IP
#      .------> port

# strategy:
# filter out everytihng which is not correct
for line in csvreader:
    correct = line[col]
    i+=1
    if (not (i % 10000) and verbose):
        print('.',end="", file=sys.stderr)
    if (not (i % 1000000) and verbose):
        print('X',end="", file=sys.stderr)

    if (correct):
        count_passed+=1
        csvwriter.writerow(line)
    else:
        count_filtered+=1

if verbose:
    print("parsed {} lines, filtered:{} OK: {}".format(i,count_filtered, count_passed), file=sys.stderr)

