#get prefixes for given AS List from CIDR Report

import urllib2
import operator
from bs4 import BeautifulSoup
COUNTRY_CODE = 'EG'

AS_LIST_TO_RANK = './'+COUNTRY_CODE+'_AS.txt'

with open(AS_LIST_TO_RANK) as f:
	ASES = f.readlines()

out_file = './'+COUNTRY_CODE+'_ASPrefixes.txt'

fo=open(out_file, 'w')

print 'out_file : '+out_file

for ASS in ASES:
	AS = ASS[0:len(ASS)-1]
	ascount=0
	url = 'http://www.cidr-report.org/cgi-bin/as-report?as='+AS+'&view=2.0'
	print
	print 'Fetch : '+url
	html_doc = urllib2.urlopen(url)
	soup = BeautifulSoup(html_doc)
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


