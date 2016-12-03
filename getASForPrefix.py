"""
Get AS of a prefixes in list.
Used selenium to browse bgp.he.net as BeautifulSoup get javascript disabled error.
Note: chromedriver path is required for selenium to work.
WARNING: Have control over no of requests made to bgp.he.net. Too many requests in a day
may lead to ip blocking.
"""

import urllib2
import operator
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

COUNTRY_CODE='EG'

out_file = './'+COUNTRY_CODE+'_ASPrefixes.txt'
fo=open(out_file, 'w')
print out_file

browser = webdriver.Chrome('/Users/Madhur/github/ASTopology/chromedriver')

with open('./prefix_list.txt') as fi:
	try:
		for line in fi:
			ll=line[:len(line)-1]
			url = 'http://bgp.he.net/net/'+ll
			print '************************************************************'
			print url

			browser.get(url)
			time.sleep(2)
			html = browser.page_source
			soup = BeautifulSoup(html)
			tbody = soup.find_all('tbody')
			print soup.prettify()

			if len(tbody)>=2:
				links = tbody[1].find_all('a')
				print links
				if len(links)>=1:
					fo.write(links[0].getText()+' '+ll+'\n')
			else:
				fo.write(ll+'\n')


	finally:
		browser.close()

