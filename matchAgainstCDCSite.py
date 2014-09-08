#!/usr/bin/env python
""" Match addresses against the CDC website
"""
import csv
import requests
import re
from bs4 import BeautifulSoup
import operator
import logging
import os

LOG_DIR = 'temp/'
HTML_DIR = 'html/'
CSV_DIR = 'csv/'
OUTPUT_DIR = 'output/'

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

logging.basicConfig(format='%(asctime)s %(levelname)s:%(name)s: %(message)s',
                    filename=LOG_DIR + 'melinta.log',
                    filemode='w',
                    level=logging.DEBUG)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

LOG = logging.getLogger(__name__)

# HTML List Indexes
ADDRESS_INDEX = 1

CITY_INDEX = 2

# CDC URL csv Indexes
STATE_INDEX = 0

URL_INDEX = 1

CDC_FILENAME = "CDC_STD_Clinics.csv"

def main():
    """docstring"""
    LOG.debug('Started')

    with open(HTML_DIR + CDC_FILENAME, 'rU') as csv_file:
        LOG.info("Reading URLs from %s", HTML_DIR+CDC_FILENAME)
        reader = csv.reader(csv_file)

        # skip the header
        reader.next()
        for rec in reader:
            state = rec[STATE_INDEX]
            url = rec[URL_INDEX]
            LOG.info("Processing %s", state)
            webpage_data = get_info_on_webpage(url)
            filename = state.replace(' ', '_')
            csv_addresses = get_addresses_from_csv(CSV_DIR + filename + ".csv")

            unique_in_webpage = [rec for rec in webpage_data
                                 if normalize_address(rec[ADDRESS_INDEX])
                                 not in csv_addresses]

            unique_in_webpage = sorted(unique_in_webpage,
                                       key=operator.itemgetter(CITY_INDEX))

            try:
                with open(OUTPUT_DIR + filename + ".csv", "wb") as csv_f:
                    writer = csv.writer(csv_f)
                    writer.writerows(unique_in_webpage)
            except UnicodeEncodeError as error:
                print "UnicodeEncode Error"
    LOG.debug('Finished')

def get_info_on_webpage(url):
    """Scrape the needed data from the CDC results page

    Look for the following fields:
    - Organization Name
    - Organization Address
    - City
    - Zipcode
    - Phone

    Args:
        url: The url of the CDC results page to scrape

    Returns:
        list(list): A list of list records containing
            Name, Address, City, Zip, Phone
    """
    soup = BeautifulSoup(requests.get(url).text)

    # Clean up <br/> tags
    for linebreak in soup.findAll('br'):
        linebreak.extract()

    info_sp = soup.findAll('table', id='resultwithin')

    organization_info = [['Name', 'Address 1', 'City', 'Zip', 'Phone']]

    for info in info_sp:
        org_name = info.find(id=re.compile("OrgLabelsHere")).text
        org_name = ' '.join(org_name.split())
        street = info.find(id=re.compile("Street1Label")).string
        city = info.find(id=re.compile("CityLabel")).string
        zipcode = info.find(id=re.compile("ZipCodeLabel")).string
        phone_label = info.find(id=re.compile("LbPhone"))
        phone = phone_label.parent.parent.findNext('td').text
        phone = phone.replace('\n', '')
        phone = re.sub(r'\(main.*', '', phone).strip()

        organization_info.append([org_name, street, city, zipcode, phone])

    return organization_info

def get_addresses_from_csv(csv_path):
    """Retrieve the addresses from the csv file

    This method looks for the 'Address 1' column in the csv and constructs
    a list of those addresses

    Args:
        csv_path: the relative path to the csv file

    Returns:
        list: The list of addresses in the 'Address 1' column
    """

    LOG.debug("Extracting addresses from csv path: %s", csv_path)

    with open(csv_path, 'rU') as csv_file:
        reader = csv.reader(csv_file)

        header = reader.next()
        if 'Address 1' in header:
            address_index = header.index('Address 1')

        addresses = []
        for rec in reader:
            addresses.append(rec[address_index])

    return addresses

def normalize_address(address):
    """Normalizes an address to make comparing easier

    Args:
        address: The address to normalize

    Returns:
        string: The normalized address
    """
    address = address.upper()

    address = re.sub(r'  *', ' ', address)
    address = re.sub(r'\.', '', address)
    address = re.sub(r'\,', '', address)

    address = re.sub(r'(\s|^)AVE(\s+|$)', r'\1AVENUE\2', address)
    address = re.sub(r'(\s|^)ST(\s+|$)', r'\1STREET\2', address)
    address = re.sub(r'(\s|^)DR(\s+|$)', r'\1DRIVE\2', address)
    address = re.sub(r'(\s|^)RD(\s+|$)', r'\1ROAD\2', address)
    address = re.sub(r'(\s|^)PL(\s+|$)', r'\1PLACE\2', address)
    address = re.sub(r'(\s|^)HWY(\s+|$)', r'\1HIGHWAY\2', address)
    address = re.sub(r'(\s|^)BLVD(\s+|$)', r'\1BOULEVARD\2', address)
    address = re.sub(r'(\s|^)RTE(\s+|$)', r'\1ROUTE\2', address)
    address = re.sub(r'(\s|^)LN(\s+|$)', r'\1LANE\2', address)

    address = re.sub(r'(\s|^)NW(\s+|$)', r'\1NORTHWEST\2', address)
    address = re.sub(r'(\s|^)N(\s+|$)', r'\1NORTH\2', address)
    address = re.sub(r'(\s|^)NE(\s+|$)', r'\1NORTHEAST\2', address)
    address = re.sub(r'(\s|^)E(\s+|$)', r'\1EAST\2', address)
    address = re.sub(r'(\s|^)SE(\s+|$)', r'\1SOUTHEAST\2', address)
    address = re.sub(r'(\s|^)S(\s+|$)', r'\1SOUTH\2', address)
    address = re.sub(r'(\s|^)SW(\s+|$)', r'\1SOUTHWEST\2', address)
    address = re.sub(r'(\s|^)W(\s+|$)', r'\1WEST\2', address)

    return address

def normalize_addresses(address_list):
    """Normalizes a list of addresses for comparison

    Uses normalize_address

    Args:
        address_list: The list of addresses to normalize

    Returns:
        list: The list of normalized addresses
    """
    return [normalize_address(address) for address in address_list]

def sorted_nicely(mylist):
    """ Sort the given iterable in the way that humans expect."""
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(mylist, key=alphanum_key)

if __name__ == "__main__":
    main()
