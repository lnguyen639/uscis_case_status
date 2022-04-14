#!/usr/bin/env python3
#Ref: http://docs.python-guide.org/en/latest/scenarios/scrape/
#Ref: https://stackoverflow.com/questions/13147914/how-to-simulate-http-post-request-using-python-requests-module
#   The first step is to look at your source page and identify the form element that is being submitted 
#   (use Firebug/Chrome/IE tools whatever (or just looking at the source)). Then find the input elements 
#   and identify the required name attributes (see above).
#   The URL you provided happens to have a "Remember Me", which although I haven't tried (because I can't), 
#   implies it'll issue a cookie for a period of time to avoid further logins -- that cookies is kept in the request.session.
#   Then just use session.get(someurl, ...) to retrieve pages etc

import requests
from bs4 import BeautifulSoup
from secret import username, passwd

SMUD_URL = 'https://myaccount.smud.org'
SMUD_BILL_URL = f'{SMUD_URL}/manage/digitalbill'
payload = {
    'UserID': username,
    'Password': passwd,
    '__RequestVerificationToken': None,
    'Lang': 'en',
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'
}
with requests.Session() as s:
    # GET from smud to get the session token
    req = s.get(SMUD_URL, headers=headers)
    page = BeautifulSoup(req.text, 'lxml')
    token = page.find('input', {'name': '__RequestVerificationToken'}).get('value')

    # Prepare payload/headers then do a POST to login
    payload['__RequestVerificationToken'] = token
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    req1 = s.post(SMUD_URL, data=payload, headers=headers)

    # Get download link for the bill
    req2 = s.get(SMUD_BILL_URL, headers=headers)
    page2 = BeautifulSoup(req2.text, 'lxml')
    bill_query = page2.find('span', {'class': 'print-link-container async-load-or-redirect'}).get('data-load-url')

    # Download bill and save to local
    req3 = s.get(f'{SMUD_URL}{bill_query}')
    page3 = BeautifulSoup(req3.text, 'lxml')
    bill_download = page3.find('a', {'class':"print-link d-block gtm-dig-bill-link-print"}).get('href')
    req4 = s.get(bill_download)
    with open('smud.pdf', 'wb') as fh:
        fh.write(req4.content)

    # Grab bill amount to print
    bill_amt = page2.find('div', {'class': 'summary-amount'}).findChild('span', {'class': 'cost-item'}).contents[0]
    print(bill_amt)
