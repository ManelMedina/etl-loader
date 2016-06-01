#!/usr/bin/env python3

import sys
import csv
import operator
import csv

"""
This script will go over all kinds of CSV files, extract a column where the country code is supposed to be and collect
all occurences of country codes.

With this list, it will then calculate the risks and add store them

Next it will calculate the average over all risks for each country and dump the result


# input format of all-place-annual.csv:

openssdp,cn,2016,243447
openssdp,tr,2016,72606
openssdp,us,2016,71080
openssdp,ar,2016,66878
openssdp,ru,2016,57472
openssdp,ve,2016,54272
openssdp,br,2016,46466
opendns,us,2016,46189
openssdp,co,2016,42616


"""

debug = True


country_risk_year = {}

with open (sys.argv[1], "r") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        country_risk_year[ (row[1],row[0],row[2]) ] = row[3]

#country_risk_year = sorted(country_risk_year)

# now country_risk_year = [ ( countrycode, risk, year ): value ]
#if debug:
#    print (repr(country_risk_year))

# extract country colume
ccs_zip = zip(*country_risk_year)
ccs = (sorted(set(list(ccs_zip)[0])))
#print(ccs)

ccs_zip = zip(*country_risk_year)
risks = sorted(set(list(ccs_zip)[1]))
#print(risks)

ccs_zip = zip(*country_risk_year)
years = sorted(set(list(ccs_zip)[2]))
#print(years)

# go through all countries in dict, calculate occurcences of risks
#print ("country,{}".format(",".join(risks)))
score= {}
print ("country,score")
for cc in ccs:
    #print("{}".format(cc), end='')
    avg=0
    for r in risks:
        for y in years:
            if ((cc,r,y) in  country_risk_year):
                avg=avg+float(country_risk_year[ (cc,r,y) ])
                #print(",{}".format(country_risk_year[ (cc,r,y) ]), end='')

            else:
                pass
                #print(",", end='')
    score[cc] = avg/len(risks)
    #print(",{}".format(score[cc]))


# dump result
writer = csv.writer(sys.stdout, delimiter=",")
writer.writerows(sorted(score.items(), key=operator.itemgetter(1)))

