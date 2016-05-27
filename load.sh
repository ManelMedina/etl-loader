#!/bin/sh

table=$1
psql iphistory -c "copy $table (ts,risk_id,ip,asn,\"place.cc\",\"place.lat\",\"place.lon\") from  STDIN delimiters ',' csv quote '''';" 


