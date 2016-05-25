#!/usr/bin/python
from __future__ import print_function
import fileinput
import radix
import sys
import argparse
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

ip_list = fileinput.input(args.filename)
tree = radix.Radix()

reader = geoip2.database.Reader('./GeoLite2-City.mmdb')

with open(prefix_table) as f:
    i=0
    for prefix in f.readlines():
        prefix, asn = prefix.strip().split()
        rnode = tree.add(prefix)
        rnode.data['origin'] = asn
        i+=1
        if (not (i % 10000) and verbose):
            print('.',end="", file=sys.stderr)
if verbose:
    print ("prefix tree loaded", file=sys.stderr)

for ip in ip_list:
    ip = ip.strip()
    if ip:
        rnode = tree.search_best(ip.strip())
        response = reader.city(ip)
        try:
            print("{ip}{sep}{asn}{sep}{cc}".format(sep=sep, ip=ip, asn=rnode.data['origin'], cc=response.country.iso_code))
        except AttributeError:
            print("{ip}{sep}0{sep}{cc}".format(sep=sep, ip=ip, cc=response.country.iso_code))    # lookup failed for example
