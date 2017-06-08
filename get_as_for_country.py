"""
Get AS list for country specified by country code.
from http://bgp.he.net
"""

import urllib2
import operator
import requests
import constants
from bs4 import BeautifulSoup

COUNTRY_CODE='IL'
url = "http://bgp.he.net/country/" + COUNTRY_CODE
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
out_file = constants.TEST_DATA + COUNTRY_CODE + '_AS.txt'

req = urllib2.Request(url, headers=hdr)

try:
    page = urllib2.urlopen(req)
except urllib2.HTTPError, e:
    print e.fp.read()

content = page.read()
soup = BeautifulSoup(content)
tbody = soup.find_all('tbody')
links = tbody[0].find_all('a')

print out_file
with open(out_file, 'w') as fo:
	for link in links:
		print link.getText()
		fo.write(link.getText().encode('utf-8')+'\n')
	fo.close()
