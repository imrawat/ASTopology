"""
Get prefixes for countries specified in AS list from cidr-report.
"""

import urllib2
import operator
import argparse
import sys
import time
import constants
from bs4 import BeautifulSoup

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description = 'get prefixes for AS from AS list')
	parser.add_argument('-c', '--country_code', help='get as prefixes', required = True)
	parser.add_argument('-ls', '--line_to_start_from', help='from where to start in AS list file. will append \
		output if argument is provided', required = False)

	args = parser.parse_args()
	COUNTRY_CODE = args.country_code
	START_LINE_NUMBER = args.line_to_start_from

	if START_LINE_NUMBER == None:
		MODE = 'w'
		START_LINE_NUMBER = 1
	else:
		MODE = 'a'
	

	AS_LIST_TO_RANK = constants.TEST_DATA + COUNTRY_CODE + '_AS.txt'

	fi = open(AS_LIST_TO_RANK)

	out_file = constants.TEST_DATA + COUNTRY_CODE + '_ASPrefixes.txt'

	fo=open(out_file, MODE)

	print 'out_file : ' + out_file

	CIDR_REPORT = "cidr-report"
	BGP_HE_NET = "bgp.he.net"

	DATA_SOURCE = CIDR_REPORT
	# DATA_SOURCE = BGP_HE_NET

	if DATA_SOURCE == BGP_HE_NET:
		from selenium import webdriver
		browser = webdriver.Chrome('/Users/Madhur/github/ASTopology/chromedriver')
	
	for i, line in enumerate(fi):
		curr_line = 0
		
		if (i + 1) < int(START_LINE_NUMBER):
			print 'skipping line ', i+1
			continue
		AS = line.strip()
		ascount=0
		if DATA_SOURCE == CIDR_REPORT:
			url = 'http://www.cidr-report.org/cgi-bin/as-report?as='+AS+'&view=2.0'
			print
			print str(i + 1)+'. Fetch : '+url
			req = urllib2.Request(url)
			try:
			    page = urllib2.urlopen(req)
			except urllib2.HTTPError, e:
			    print e.fp.read()

			content = page.read()
			soup = BeautifulSoup(content)
			uls = soup.find_all('ul')
			pres = uls[2].find_all('pre')
			print len(pres)
			if len(pres)<2:
				continue
			links = pres[1].find_all('a')
			for link in links[1:]:
				classes = link['class']
				colorclass = classes[0]
				if(colorclass=='green' or colorclass=='black'):
					print link.getText()
					fo.write(AS+' '+link.getText()+'\n')
					break
			time.sleep(8)
		elif DATA_SOURCE == BGP_HE_NET:
			url = "http://bgp.he.net/" + AS + "#_prefixes"
			print
			print str(i + 1)+'. Fetch : '+url
			browser.get(url)
			time.sleep(4)
			html = browser.page_source
			soup = BeautifulSoup(html)
			tbodys = soup.find_all('tbody')
			
			if len(tbodys) > 1:
				
				trs = tbodys[1].find_all("tr")
				print len(tbodys)

			else:
				print "len(tbody) " + str(len(tbody))
				exit()
			if len(trs) > 0:
				links = trs[0].find_all('a')
			else:
				print "len(trs) " + str(len(trs))
				exit()
			if len(links) > 0:
				link = links[0].getText().encode('utf-8')
				print link
				fo.write(AS + " " + link + "\n")
			else:
				print "len(links) " + str(len(links))
				exit()

	fo.close()