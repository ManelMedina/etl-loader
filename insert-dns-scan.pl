#!/usr/bin/perl

use Geo::IP;
use Geo::IP::Record;

my $path = "/usr/share/GeoIP/";
my $gi = Geo::IP->open("$path/GeoLiteCity.dat", GEOIP_STANDARD) || die "could not open GeoIPv4 DB";
#my $giA = Geo::IP->open("$path/GeoIPASNum.dat", GEOIP_STANDARD) || die "could not open GeoIP ASN DB";


my $indicator = "cc2afece";	# we can grep for that in the output actually


my $risk_id = 1;



while ($ln = <STDIN>)
{
	chomp $ln;
##
## IP1:53:64.21.0.0:NULL:1367107201.262564:0:0:0

# DB structure:
#create table hits (ts timestamp with time zone not null, risk_id integer not null references risk(id), ip inet not null, "place.cc" varchar(2), "place.lat" float, "place.lon" float);

  ($junk,$port,$pri_ip,$alt_ip,$time_t,$rcode,$ra,$correct,$tc) = split ( /:/, $ln);
	$lines++;
	$ip_hash{$pri_ip}++;
	if (!($alt_ip eq "NULL"))
	{
		$alternate_responders++;
		$ip_hash{$alt_ip}++;
	}
	if (!($port == 53))
	{
		$wrong_port++;
	}
	if ($rcode == 0)
	{
		$rcode_ok++;
	}
	if ($rcode == 1)
	{
		$rcode_formerr++;
	}
	if ($rcode == 2)
	{
		$rcode_servfail++;
	}
	if ($rcode == 3)
	{
		$rcode_namefail++;
	}
	if ($rcode == 4)
	{
		$rcode_notimp++;
	}
	if ($rcode == 5)
	{
		$rcode_refused++;
	}
	if ($ra == 1)
	{
		$ra_count++;
	}
	if ($correct == 1)
	{
		$correct_count++;
	}
	if ($tc == 1)
	{
		$tc_count++;
	}
	if ($correct == 1 and $rcode == 0)
	{
		# count as correct and actually insert into DB
	    $record = $gi->record_by_addr($pri_ip);	
		#$recordA = $giA->record_by_addr($pri_ip);
		if (not defined($record)) 
		{
			$geo_lat = 'NULL';
			$geo_lon = 'NULL';
			$geo_cc = 'NULL';
		}
		else {
			$geo_cc = $record->country_code;
			$geo_lat = $record->latitude;
			$geo_lon = $record->longitude;
		}
		
		print "INSERT into hits VALUES ( to_timestamp($time_t), $risk_id, '$pri_ip', '$geo_cc', $geo_lat, $geo_lon);\n";
	}
}

foreach $key (keys %ip_hash) {
	$uniq++;
	if ($ip_hash{$key} > 1) {
		$dupe++;
	}
}
print "SUMMARY\n";
print "$lines servers responded to udp/53 probe\n";
print "$uniq unique IPs\n";
print "$dupe IPs responded more than once\n";
print "$alternate_responders servers responded from a different IP than probed\n";
print "$correct_count gave the correct answer to the A? for the DNS name queried\n";
print "$wrong_port responded from a source port other than udp/53\n";
print "$ra_count responses had recursion-available bit set\n";
print "\n";
print "$rcode_ok returned OK (RCODE=0)\n";
print "$rcode_formerr returned FORMERR (RCODE=1)\n";
print "$rcode_servfail returned SERVFAIL (RCODE=2)\n";
print "$rcode_namefail returned NAMEFAIL (RCODE=3)\n";
print "$rcode_notimp returned NOTIMP (RCODE=4)\n";
print "$rcode_refused returned REFUSED (RCODE=5)\n";


print "SQL:INSERT INTO statistics VALUES (\'$ARGV[0]\', $lines, $uniq, $dupe, $alternate_responders, $correct_count, $wrong_port, $ra_count, $rcode_ok, $rcode_formerr, $rcode_servfail, $rcode_namefail, $rcode_notimp, $rcode_refused, $tc_count);:\n"; 
