"""
Scrape conesize from caida.org.
This should be used intead of fetching conesize for each individual AS.
"""


import urllib2
import operator
import requests
import sys
import re

from bs4 import BeautifulSoup

fo = open("consize.txt", "w")

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

url = "http://as-rank.caida.org/?mode0=as-ranking&n=200&ranksort=1"
req = urllib2.Request(url, headers=hdr)
try:
    page = urllib2.urlopen(req)
except urllib2.HTTPError, e:
    print e.fp.read()

content = page.read()
soup = BeautifulSoup(content)

tables = soup.find_all("table")
if len(tables) < 1:
	print "tables len " + str(len(tables))
	exit()

trs = tables[0].find_all('tr')
if len(trs) < 5:
	print "trs len " + str(len(trs))
	exit()
for tr in trs[3:len(trs)-1]:
	tds = tr.find_all('td')
	if len(tds) < 6:
		print "tds len " + str(len(tds))
		continue
	asnum = (tds[1].getText().strip())
	consizestr = (tds[5].getText().strip())
	consize = re.sub('[^0-9]', '', consizestr)
	towrite = asnum + " " + consize + "\n"
	print towrite
	fo.write(towrite)

fo.close()





