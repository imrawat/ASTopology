#get prefixes for given AS List from CIDR Report

import urllib2
import operator
from bs4 import BeautifulSoup

AS_LIST_TO_RANK = './AS_NUMBER.txt'

with open(AS_LIST_TO_RANK) as f:
	ASES = f.readlines()

fo=open('./AS_prefixes.txt', 'w')

for ASS in ASES:
	AS = ASS[0:len(ASS)-1]
	ascount=0
	url = 'http://www.cidr-report.org/cgi-bin/as-report?as='+AS+'&view=2.0'
	print 'Ranking '+AS
	html_doc = urllib2.urlopen(url)
	soup = BeautifulSoup(html_doc)
	uls = soup.find_all('ul')
	pres = uls[2].find_all('pre')
	links = pres[1].find_all('a')
	for link in links[1:]:
		classes = link['class']
		colorclass = classes[0]
		if(colorclass=='green' or colorclass=='black'):
			print link.text()
