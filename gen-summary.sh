#!/usr/bin/env bash

# Risk IDs:
# id |   name
#----+----------
#  1 | opendns
#  2 | openntp
#  3 | spam
#  4 | opensnmp
#  5 | openssdp

declare -A risks=( ["1"]="opendns" ["2"]="openntp" ["3"]="spam" ["4"]="opensnmp" ["5"]="openssdp" )

rate=1000
YEAR="1=1"
YEAR="ts >= date('2016-01-01')"
YEAR2="1=1"
YEAR2=$YEAR

for rid in ${!risks[@]}; do 
	val=${risks[$rid]}

	# by country, annual
	outfile="$val-place-annual.csv"
	echo "select  extract(year from date_trunc('year', ts)) as year, lower(\"place.cc\") as country, $rate*count(*) as value  from hits "\
		"where $YEAR AND risk_id=$rid group by year,country order by value desc;" | \
		psql -t -F"," -A iphistory > $outfile

	# by country, monthly
	outfile="$val-place-monthly.csv"
	echo "select  date(date_trunc('month', ts)) as date, lower(\"place.cc\") as country, $rate*count(*) as value  from hits "\
		"where $YEAR2 AND risk_id=$rid group by date,country order by value desc;" | \
		psql -t -F"," -A iphistory > $outfile

	# by ASN, annual
	outfile="$val-asn-annual.csv"
	echo "select  extract(year from date_trunc('year', ts)) as year, asn as asn, $rate*count(*) as value  from hits "\
		"where $YEAR AND risk_id=$rid group by year,asn order by value desc;" | \
		psql -t -F"," -A iphistory > $outfile

	# by ASN, monthly
	outfile="$val-asn-monthly.csv"
	echo "select  date(date_trunc('month', ts)) as date, asn as asn, $rate*count(*) as value  from hits "\
		"where $YEAR2 AND risk_id=$rid group by date,asn order by value desc;" | \
		psql -t -F"," -A iphistory > $outfile
done

# Overall file with all risks in one
outfile="all-place-annual.csv"
echo "select risk.name as risk_name, lower(\"place.cc\") as country, extract(year from date_trunc('year', ts)) as year, $rate*count(*) as value  from risk,hits "\
	"where $YEAR AND risk_id=risk.id group by risk_name,year,country order by value desc;" | \
	psql -t -F"," -A iphistory > $outfile

outfile="places.csv"
src/extract_places.py all-place-annual.csv > $outfile
