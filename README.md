# Overview of the ETL process

ETL ([Extract, Transform, Load](https://en.wikipedia.org/wiki/Extract,_transform,_load)) is a standard process
in data warehousing applications.

In our case, we need to do a bit more:
  - extract data (gzipped) 
  - sample data: only print every x'th line (this is an optional step)
  - filter it : remove lines which are not true vulnerable IP addresses (no open recursive nameserver, SNMP, etc)
  - parse the respective format and bring into an internal standardized CSV format
  - enrich the data: add ASN, country code info
  - load the data into the postgresql DB


call syntax (snmp data in our case):
```

$ zcat infile_snmp.gz | sample.py | \
$ filter_snmp.py | parse_snmp.py | enrich.py | load.py tablename

```

A more concrete example would be:
```
$ zcat data/snmp-data/parsed.20160524.out.gz | sample.py -n 10 | src/parse_snmp.py > tmp.20160524.out
$ cat tmp.20160524.out | src/enrich.py -v -s , -c 2 - | src/load.sh hits
```

Note the head -n 10 for testing.


# Aggregation

Once loaded into the postgresql DB, we easily calculate aggregates:

```
$ gen-summary.sh
```



# How to run the ETL process?

Take a look at run.sh, adapt and run it.


