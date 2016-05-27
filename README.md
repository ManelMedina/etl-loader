# Overview of the ETL process

ETL ([Extract, Transform, Load](https://en.wikipedia.org/wiki/Extract,_transform,_load)) is a standard process
in data warehousing applications.

In our case, we need to do a bit more:
  - extract data (gzipped) 
  - filter it : remove lines which are not true vulnerable IP addresses (no open recursive nameserver, SNMP, etc)
  - parse the respective format and bring into an internal standardized CSV format
  - enrich the data: add ASN, country code info
  - load the data into the postgresql DB


call syntax (snmp data in our case):
```

$ zcat infile_snmp.gz | \
$ filter_snmp.py | parse_snmp.py | enrich.py | load.py tablename

```

A more concrete example would be:
```
$ time zcat data/snmp-data/parsed.20160524.out.gz | head -n 10 | src/parse_snmp.py | src/enrich.py -v -s , -c 2 - | src/load.sh hits
```

Note the head -n 10 for testing.


# Aggregation

Once loaded into the postgresql DB, we easily calculate aggregates:

```
$ gen-summary.sh
```



