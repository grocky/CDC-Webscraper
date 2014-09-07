#!/usr/bin/env bash

function getAddresses() {
    awk -F"," '{
        if ($16 ~ /^"/) {
            $address = $16 $17;
            gsub(/"/, "", $address);
        } else {
            $address = $16
        }
        gsub(/ +/, " ", $address);
        gsub(/\./, "", $address);
        $address = toupper($address);

        gsub(/ AVE$/, " AVENUE", $0);
        gsub(/ AVE /, " AVENUE ", $0);
        gsub(/ ST$/, " STREET", $0);
        gsub(/ ST /, " STREET ", $0);
        gsub(/ DR$/, " DRIVE", $0);
        gsub(/ DR /, " DRIVE ", $0);
        gsub(/ RD$/, " ROAD", $0);
        gsub(/ RD /, " ROAD ", $0);
        gsub(/ PL$/, " PLACE", $0);
        gsub(/ PL /, " PLACE ", $0);
        gsub(/ HWY$/, " HIGHWAY", $0);
        gsub(/ HWY /, " HIGHWAY ", $0);
        gsub(/ BLVD$/, " BOULEVARD", $0);
        gsub(/ BLVD /, " BOULEVARD ", $0);
        gsub(/ RTE$/, " ROUTE", $0);
        gsub(/ RTE /, " ROUTE ", $0);
        gsub(/ LN$/, " LANE", $0);
        gsub(/ LN /, " LANE ", $0);

        gsub(/ NW /, " NORTHWEST ", $0);
        gsub(/ NW$/, " NORTHWEST", $0);
        gsub(/ N /, " NORTH ", $0);
        gsub(/ N$/, " NORTH", $0);
        gsub(/ NE /, " NORTHEAST ", $0);
        gsub(/ NE$/, " NORTHEAST", $0);
        gsub(/ E /, " EAST ", $0);
        gsub(/ E$/, " EAST", $0);
        gsub(/ SE /, " SOUTHEAST ", $0);
        gsub(/ SE$/, " SOUTHEAST", $0);
        gsub(/ S /, " SOUTH ", $0);
        gsub(/ S$/, " SOUTH", $0);
        gsub(/ SW /, " SOUTHWEST ", $0);
        gsub(/ SW$/, " SOUTHWEST", $0);
        gsub(/ W /, " WEST ", $0);
        gsub(/ W$/, " WEST", $0);

        print $address
    }' csv/$1.csv | grep -v '^Address [0-9]$' | sort -u
}

getAddresses $1;