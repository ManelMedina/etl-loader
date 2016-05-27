#!/bin/sh

DOW=`date +%a`

wget -q -O new.table-v4.txt.$DOW lg01.infra.ring.nlnog.net/table-v4.txt
wget -q -O new.table-v6.txt.$DOW lg01.infra.ring.nlnog.net/table-v6.txt

cat new.table-v4.txt.??? | sort -u > table-v4.txt
cat new.table-v6.txt.??? | sort -u > table-v6.txt

