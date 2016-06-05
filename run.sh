#!/bin/bash

# sample rate
rate=1000

## snmp
#for f in data/snmp-data/parsed*.out.gz; do
#	echo 
#	echo "Processing SNMP...... $f"
#	echo 
#	time ( zcat $f | src/sample -n $rate | src/filter_snmp.py | awk -F: '// { print $1 ":" $2; }' | src/parse_snmp.py > tmp.out; cat tmp.out | src/enrich.py -v -s , -c 2 - | src/load.sh hits )
#	echo "=================================="
#done

## dns
## zcat ./data/dns-scan/parsed.20160508.out.gz | src/sample -n 1000 | src/filter_dns.py | src/parse_dns.py > tmp.out
for f in data/dns-scan/parsed*.out.gz; do
	echo 
	echo "Processing DNS...... $f"
	echo 
	time ( zcat $f | src/sample -n $rate | src/filter_dns.py | src/parse_dns.py > tmp.out; cat tmp.out | src/enrich.py -v -s , -c 2 - | src/load.sh hits )
	echo "=================================="
done

# ntp
for f in data/ntp-scan/parsed.*.out.gz; do
	echo 
	echo "Processing NTP...... $f"
	echo 
	# note: this data is already sampled 1:1000
	time ( zcat $f | src/filter_ntp.py | src/parse_ntp.py > tmp.out; cat tmp.out | src/enrich.py -v -s , -c 2 - | src/load.sh hits )
	echo "=================================="
done

# spam
for f in data/spam/*.csv.gz; do
	echo 
	echo "Processing Spam...... $f"
	echo 
	time ( zcat $f | src/sample -n $rate | src/filter_spam.py | src/parse_spam.py > tmp.out; cat tmp.out | src/enrich.py -v -s , -c 2 - | src/load.sh hits )
	echo "=================================="
done


# ssdp
for f in data/ssdp-data/*.out.gz; do
	echo 
	echo "Processing SSDP...... $f"
	echo 
	time ( zcat $f | src/sample -n 1000 | src/filter_ssdp.py | src/parse_ssdp.py > tmp.out; cat tmp.out | src/enrich.py -v -s , -c 2 - | src/load.sh hits )
	echo "=================================="
done

#rm tmp.out
