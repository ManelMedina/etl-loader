#!/usr/bin/env python

"""
 No operation for now
 For snmp data we can do that with a simple sh script:
 psql iphistory -c "copy hits (ts,risk_id,ip,asn,\"place.cc\") from  STDIN delimiters ',' csv quote '''';" < infile

"""

