#!/bin/sh

wget --header="Accept: text/tab-separated-values" -O cty2pop.tsv \
	"https://query.wikidata.org/sparql?query=select%20%3Fc%20%3Fisoc2%20%3Fisoc3%20%3Fpop%20where%20%7B%0A%20%20%09%3Fc%20wdt%3AP297%20%3Fisoc2%20.%0A%20%20%20%20%3Fc%20wdt%3AP298%20%3Fisoc3%20.%0A%09%3Fc%20wdt%3AP1082%20%3Fpop%0A%7D"

awk '// { print $2 "," $4; }' < cty2pop.tsv > cty2pop.csv
sed -i 's/"//g' cty2pop.csv
awk -F "\^" ' { print $1; }' < cty2pop.csv | \
	tail -n +2 >  c
mv c cty2pop.csv

rm cty2pop.tsv

# create table country (cc varchar(2) primary key, population integer, internet_users integer, fixed_broadband_subscribers integer, ips integer, gdp_per_capita_ppp float, gni_ppp float);
# 
# COPY table_name [ ( column_name [, ...] ) ]
#    FROM { 'filename' | PROGRAM 'command' | STDIN }
#    [ [ WITH ] ( option [, ...] ) ]


# note here we have some duplicates maybe, need to address this

cwd=$(pwd)
psql iphistory -c "copy country (cc, population) from '$cwd/cty2pop.csv' with csv;"
