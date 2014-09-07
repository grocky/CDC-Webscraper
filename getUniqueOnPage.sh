#!/usr/bin/env bash

./getAddresses.sh $1 > $1.csv
./getAddressesOnPage.sh $1 > $1.page

comm -1 -3 $1.csv $1.page > $1_uniqueOnPage.txt

#rm $1.csv $1.page
