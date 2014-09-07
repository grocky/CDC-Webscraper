#!/usr/bin/env bash

function getAddressesOnPage() {

    grep 'Street1Label' html/$1.html |
     awk '{
        gsub(/^.*Street1Label">/, "", $0);
        gsub(/<\/span>/, "", $0);
        gsub(/ +/, " ", $address);
        gsub(/\./, "", $address);
        $0 = toupper($0);

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

        print $0
    }' | sort -u
}

getAddressesOnPage $1