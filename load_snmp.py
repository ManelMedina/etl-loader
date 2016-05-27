#!/usr/bin/env python


import sys
import argparse
import psycopg2

# input file format:
#  Date, Country, Value, Normalized
# example:
#  2016,CN,818951
#  2016,IN,725405
#  2016,IR,613830

# call syntax:
#  filter.py < infile | parse.py | enrich.py | load.py tablename
# then aggregate from DB:
#  aggregate.sh 
#


