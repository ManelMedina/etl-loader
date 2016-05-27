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
1462233601:129.1.0.0:NULL:'0$     public              0 0   +    '
1462233601:96.3.0.0:NULL:'0$     public    `         0 0   +    '
1462233601:96.3.0.0:NULL:'0$     public    `         0 0   +    '
1462233601:216.12.22.158:216.12.0.0:'0$     public              0 0   +    '
1462233601:216.12.22.158:216.12.0.0:'0$     public              0 0   +    '
1462233601:72.22.0.0:NULL:'0$     public    H         0 0   +    '
1462233601:72.22.0.0:NULL:'0$     public    H         0 0   +    '
1462233601:72.26.0.0:NULL:'0$     public    H         0 0   +    '
1462233601:72.26.0.0:NULL:'0$     public    H         0 0   +    '
1462233601:8.18.0.0:NULL:'0$     public              0 0   +    '
1462233601:8.18.0.0:NULL:'0$     public              0 0   +    '
1462233601:96.18.0.0:NULL:'0$     public    `         0 0   +    '
1462233601:96.18.0.0:NULL:'0$     public    `         0 0   +    '
1462233601:50.25.0.0:NULL:'0$     public    2         0 0   +    '
1462233601:50.25.0.0:NULL:'0$     public    2         0 0   +    '
1462233601:135.26.0.0:NULL:'0$     public              0 0   +    '
1462233601:135.26.0.0:NULL:'0$     public              0 0   +    '
1462233601:193.9.0.0:1.205.2.4:'0        public                0   0     +          Cisco IOS Software, C2951 Software (C2951-UNIVERSALK9-M), Version 15.1(4)M4, RELEASE SOFTWARE (fc1)  Technical Support\: http\://www.cisco.com/techsupport  Copyright (c) 1986-2012 by Cisco Systems, Inc.  Compiled Tue 20-Mar-12 19\:11 by prod_rel_team0   +         +        0   +       C L   0   +         0   +         uklocnint.aveva.com0   +         0   +         N0   +       C  0   +           +        0   +           +      s'
1462233601:193.9.0.0:1.24.2.4:'0  '     public                0   0     +          Cisco IOS Software, C2951 Software (C2951-UNIVERSALK9-M), Version 15.1(4)M4, RELEASE SOFTWARE (fc1)  Technical Support\: http\://www.cisco.com/techsupport  Copyright (c) 1986-2012 by Cisco Systems, Inc.  Compiled Tue 20-Mar-12 19\:11 by prod_rel_team'
1462233601:209.33.0.0:NULL:'0$     public     !        0 0   +    '
1462233601:209.33.0.0:NULL:'0$     public     !        0 0   +    '
"""

# Explanation / need to understand:
# timestamp (epoche) UTC : ip addr : second IP : snmp string/snmp data


reader = csv.reader(sys.stdin, delimiter=':', quotechar="'")
for line in reader:
    ts=float(line[0])
    # postgresql format: 2016-05-08 02:00:04.126444+02
    ts = time.strftime("%Y-%m-%d %H:%M:%S.0+00", time.localtime(ts))     # remember, we are UTC 
    ip = line[1]
    print("'{ts}'{sep}{risk}{sep}'{ip}'".format(sep=sep,risk=4,ts=ts,ip=ip))


