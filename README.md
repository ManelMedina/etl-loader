# Overview of the ETL process

ETL ([Extract, Transform, Load](https://en.wikipedia.org/wiki/Extract,_transform,_load)) is a standard process
in data warehousing applications.

In our case, we need to 
  - extract data (gzipped) 
  - filter it : remove lines which are not true vulnerable IP addresses (no open recursive nameserver, SNMP, etc)
  - parse the respective format and bring into an internal standardized CSV format
  - enrich the data: add ASN, country code info
  - load the data into the postgresql DB


call syntax:
```

$ filter.py < infile | parse.py | enrich.py | load.py tablename

```

# Aggregation

Once loaded into the postgresql DB, we easily calculate aggregates:

```
$ gen-summary.sh
```



