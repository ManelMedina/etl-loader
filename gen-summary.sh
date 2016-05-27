#!/bin/sh

# DNS

# by country
# opendns-place-annual.csv
echo "select  extract(year from date_trunc('year', ts)) as year, \"place.cc\" as country, count(*) as value  from hits group by year,country order by value desc;" | \
	psql -t -F"," -A iphistory > opendns-place-annual.csv

# opendns-place-monthly.csv
echo "select  date_trunc('month', ts) as date, \"place.cc\" as country, count(*) as value  from hits group by date,country order by value desc;" | \
	psql -t -F"," -A iphistory > opendns-place-monthly.csv

# by ASN
# opendns-place-annual.csv
echo "select  extract(year from date_trunc('year', ts)) as year, asn as asn, count(*) as value  from hits group by year,asn order by value desc;" | \
	psql -t -F"," -A iphistory > opendns-asn-annual.csv

# opendns-place-monthly.csv
echo "select  date_trunc('month', ts) as date, asn as asn, count(*) as value  from hits group by date,asn order by value desc;" | \
	psql -t -F"," -A iphistory > opendns-asn-monthly.csv
