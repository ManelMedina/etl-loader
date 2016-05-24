#!/usr/bin/python
"""
    Job Snijders
    IP 2 ASN converter
"""

"""
    the prefix table file has the following format: one prefix and origin
    per line, separated by a space. Example:

    $ cat bgp-table-v4
    8.8.8.0/24 15169
    94.142.240.0/21 8283
    $
"""

prefix_table = "/home/jared/generic/table-v4.txt"

import fileinput
import radix

ip_list = fileinput.input()
tree = radix.Radix()

with open(prefix_table) as f:
    for prefix in f.readlines():
        prefix, asn = prefix.strip().split()
        rnode = tree.add(prefix)
        rnode.data['origin'] = asn

for ip in ip_list:
    ip = ip.strip()
    rnode = tree.search_best(ip.strip())
    try:
        print "%s|%s" % (ip, rnode.data['origin'])
    except AttributeError:
        print "%s|0" % ip # lookup failed for example
