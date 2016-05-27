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

for rid in ${!risks[@]}; do 
	val=${risks[$rid]}

	# by country, annual
	outfile="$val-place-annual.csv"
	echo "select  extract(year from date_trunc('year', ts)) as year, \"place.cc\" as country, count(*) as value  from hits where risk_id=$rid group by year,country order by value desc;" | \
		psql -t -F"," -A iphistory > $outfile

	# by country, monthly
	outfile="$val-place-monthly.csv"
	echo "select  date(date_trunc('month', ts)) as date, \"place.cc\" as country, count(*) as value  from hits where risk_id=$rid group by date,country order by value desc;" | \
		psql -t -F"," -A iphistory > $outfile

	# by ASN, annual
	outfile="$val-asn-annual.csv"
	echo "select  extract(year from date_trunc('year', ts)) as year, asn as asn, count(*) as value  from hits where risk_id=$rid group by year,asn order by value desc;" | \
		psql -t -F"," -A iphistory > $outfile

	# by ASN, monthly
	outfile="$val-asn-monthly.csv"
	echo "select  date(date_trunc('month', ts)) as date, asn as asn, count(*) as value  from hits where risk_id=$rid group by date,asn order by value desc;" | \
		psql -t -F"," -A iphistory > $outfile
done

# Overall file with all risks in one
outfile="all-place-annual.csv"
echo "select risk.name as risk_name, extract(year from date_trunc('year', ts)) as year, \"place.cc\" as country, count(*) as value  from risk,hits where risk_id=risk.id group by risk_name,year,country order by value desc;" | \
	psql -t -F"," -A iphistory > $outfile

