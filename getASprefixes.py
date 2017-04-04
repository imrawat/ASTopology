"""
Get prefixes for countries specified in AS list from cidr-report.
"""

import urllib2
import operator
import sys
import time
from bs4 import BeautifulSoup
from selenium import webdriver

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

browser = webdriver.Chrome('/Users/Madhur/github/ASTopology/chromedriver')

if __name__ == "__main__":

	if len(sys.argv) < 4:
		print "Usage: python getASPrefixes.py <COUNTRY_CODE> <startASIndex> <endASIndex>"
		exit()

	startASIndex = int(sys.argv[2])
	endASIndex = int(sys.argv[3])
	COUNTRY_CODE = sys.argv[1]

	if startASIndex==1:
		MODE = 'w'
	else:
		MODE = 'a'

	

	AS_LIST_TO_RANK = './'+COUNTRY_CODE+'_AS.txt'

	with open(AS_LIST_TO_RANK) as f:
		ASES = f.readlines()

	out_file = './'+COUNTRY_CODE+'_ASPrefixes.txt'

	fo=open(out_file, MODE)

	print 'out_file : '+out_file

	CIDR_REPORT = "cidr-report"
	BGP_HE_NET = "bgp.he.net"

	# DATA_SOURCE = CIDR_REPORT
	DATA_SOURCE = BGP_HE_NET



	counter = 1
	print startASIndex
	print endASIndex
	
	for ASS in ASES:
		if counter>=startASIndex and counter<=endASIndex:

			AS = ASS[0:len(ASS)-1]
			ascount=0
			if DATA_SOURCE == CIDR_REPORT:
				url = 'http://www.cidr-report.org/cgi-bin/as-report?as='+AS+'&view=2.0'
				print
				print str(counter)+'. Fetch : '+url
				req = urllib2.Request(url, headers=hdr)
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
			elif DATA_SOURCE == BGP_HE_NET:
				url = "http://bgp.he.net/" + AS + "#_prefixes"
				print
				print str(counter)+'. Fetch : '+url
				browser.get(url)
				time.sleep(4)
				html = browser.page_source
				soup = BeautifulSoup(html)
				tbodys = soup.find_all('tbody')
				
				if len(tbodys) > 1:
					
					trs = tbodys[1].find_all("tr")
					print len(tbodys)
					
					# for tbody in tbodys:
					# 	print "******************"
					# 	print tbody
					# 	print "******************"
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

		counter=counter+1		
	fo.close()
		


