#!/usr/bin/python
from __future__ import print_function
import fileinput
import radix
import sys
import argparse
import csv
import geoip2.database


"""
  enrich.py
  Based on work by
    Job Snijders
    IP 2 ASN converter
  as well as Jared Mauch whom I own a big thank you for support and help

  This script does two things to a log line:
    1. specified by the cmd line parameter, it will look for an ip address in a given column of a csv file
    2. extract the ip address and enrich the CSV file by appending
       ....;<country_code>;ASN
       of that specific IP address.

    Note that currently, only one colume containing IP address info can be given

    In order to do the IP2asn lookup, a CIDR -> ASN table ("prefix table") is needed.
    See the enclosed update.sh script for an example where to get this info from.
    Basically it comes for BGP routers.

    The prefix table file has the following format: one prefix and origin
    per line, separated by a space. Example:

    ```
    $ cat bgp-table-v4
    8.8.8.0/24 15169
    94.142.240.0/21 8283
    $
    ```

    In order to do proper IP 2 country code lookups, rely on maxmind's geoip database:
    https://geoip2.readthedocs.io/en/latest/

"""

prefix_table = "./table-v4.txt"
sep=";"
verbose = False


parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose',   action='store_true', help="turn on verbose mode.")
parser.add_argument('-s', '--separator', type=str, default=sep, help='CSV file field separator.')
parser.add_argument('-c', '--column',    type=int, help='Column number (counting from 0) where the ip address is stored in the CSV file.')
parser.add_argument('filename',  help='A CSV file with a column containing IP addresses. Use "-" as filename if you want to read from stdin.')

args = parser.parse_args()

if args.verbose:
    verbose = True
if args.separator:
    sep = args.separator
if args.column:
    col = args.column

infile = fileinput.input(args.filename)
tree = radix.Radix()

reader = geoip2.database.Reader('./GeoLite2-City.mmdb')
#
# loading of BGP table
#
with open(prefix_table) as f:
    i=0
    for prefix in f.readlines():
        prefix, asn = prefix.strip().split()
        #if verbose: print ("prefix,asn={prefix},{asn}".format(prefix=prefix,asn=asn), file=sys.stderr)
        rnode = tree.add(prefix)
        rnode.data['origin'] = int(asn)
        i+=1
        if (not (i % 10000) and verbose):
            print('.',end="", file=sys.stderr)
if verbose:
    print ("prefix tree loaded", file=sys.stderr)


#
# parse main file
#
i=0
count_no_country=0
count_unknown_asns=0
csvreader = csv.reader(infile, delimiter=',', quotechar="'")
csvwriter = csv.writer(sys.stdout, delimiter=',', quotechar="'") #, quoting=csv.QUOTE_MINIMAL)
for line in csvreader:
    ip = line[col]
    i+=1
    if (not (i % 10000) and verbose):
        print('.',end="", file=sys.stderr)
    if (not (i % 1000000) and verbose):
        print('X',end="", file=sys.stderr)

    #if verbose: print("ip={}".format(ip))
    ip = ip.strip()
    if ip:
        rnode = tree.search_best(ip.strip())
        if rnode:
            line.append(rnode.data['origin'])
        else:
            line.append('')
            count_unknown_asns+=1
        try:
            response = reader.city(ip)
            line.append(response.country.iso_code)
            #line.append(response.location.latitude)
            #line.append(response.location.longitude)
        except:
            line.append('XY')
            count_no_country+=1

        csvwriter.writerow(line)

print("parsed {} lines, could not find {} country places. {} unknown ASNs".format(i,count_no_country, count_unknown_asns), file=sys.stderr)

