#!/usr/local/bin/python2.7
#Ref: http://docs.python-guide.org/en/latest/scenarios/scrape/
#Ref: https://stackoverflow.com/questions/13147914/how-to-simulate-http-post-request-using-python-requests-module

import requests
from lxml import html
import argparse

a = argparse.ArgumentParser()
a.add_argument('-r', help="WAC receipt number", required=True)
args = a.parse_args()

URL = 'https://egov.uscis.gov/casestatus/mycasestatus.do'
payload = {
    'appReceiptNum': args.r, #7'
    'initCaseSearch': 'CHECK STATUS'
}
session = requests.session()
r = requests.post(URL, data=payload)
#print r.cookies
tree = html.fromstring(r.content)
info = tree.xpath('//div[@class="rows text-center"]/p/text()')
print info
