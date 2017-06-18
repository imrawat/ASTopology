from bs4 import BeautifulSoup
import constants
import re
import urllib2

url = constants.TEST_DATA + "aggregationreport.htm"
print 'in_file', url
fi = open(url)
out_file = constants.TEST_DATA + "announced_prefixes.txt"
print 'out_file', out_file
fo = open(out_file, "w")
# page = open(url)
# soup = BeautifulSoup(page.read())
# print soup

for line in fi:
	line = line.strip()
	splits = line.split()
	splits2 = splits[1].split('<')
	# print splits
	splits3 = splits2[0].split('>')
	print splits3[1], splits[len(splits) - 3]
	fo.write(splits3[1] + " " + splits[len(splits) - 3] + "\n")
fo.close()