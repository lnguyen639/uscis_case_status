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
import argparse
from bs4 import BeautifulSoup
from secret import username, passwd

URL = 'https://myaccount.smud.org/?Length=0'
URL = 'https://myaccount.smud.org/?ack=true/'
URL = 'https://myaccount.smud.org/signin/index?ReturnUrl=%2fmanage%2fresidential%2fdashboard'
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
    req = s.get(URL, headers=headers)
    page = BeautifulSoup(req.text)
    token = page.find('input', {'name': '__RequestVerificationToken'}).get('value')
    payload['__RequestVerificationToken'] = token
    headers['Content-Type'] = 'application/x-www-form-urlencoded'

    req1 = s.post(URL, data=payload, headers=headers)
    print(req1.content)
