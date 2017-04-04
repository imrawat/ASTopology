'''
Get consize for AS list
append(a) : get consize for only prefixes for which its not saved 
'''

BASE_URL = "http://as-rank.caida.org/?mode0=as-info&mode1=as-table&as="
AS_FILE = "all_as.txt"
outfile = "all_as_consize.txt"
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

import urllib2
import operator
import requests
import sys
from bs4 import BeautifulSoup

if len(sys.argv) < 2:
	print "Usage: python getConesize.py <mode append(a)/write(w)>"
	exit()

inmode = sys.argv[1]
# if inmode == "A" or inmode == "a":
# 	mode = "a"
# else if inmode == "W" or inmode == "w":
# 	mode = "w"
lines = []
with open(outfile) as fi:
	for line in fi:
		lines.append(line)

fo = open(outfile, 'w')
lnum = 0

for line in lines:
	lnum = lnum + 1
	line = line.strip()
	splits = line.split()
	if len(splits) > 1 and (inmode == "A" or inmode == "a"):
		fo.write(line + '\n')
		print str(lnum) + " already for " + split[0]
		continue
	AS = splits[0]
	url = BASE_URL + AS
	print url
	req = urllib2.Request(url, headers=hdr)
	try:
	    page = urllib2.urlopen(req)
	except urllib2.HTTPError, e:
	    print e.fp.read()

	content = page.read()
	soup = BeautifulSoup(content)
	tbodys = soup.find_all('tbody')
	if len(tbodys) < 2:
		print "tbodys len " + str(len(tbodys))
		continue
	trs = tbodys[1].find_all('tr')
	if len(trs) < 6:
		print "trs len " + str(len(trs))
		continue
	tds = trs[5].find_all('td')
	if len(tds) < 1:
		print "tds len " + str(len(tds))
		continue
	consize = tds[0].getText().strip()
	fo.write(AS + ' ' + consize + " \n")
