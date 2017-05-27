from bs4 import BeautifulSoup
import re
import urllib2

fo = open("AnnouncedPrefixes.txt", "w")


url = "/Users/Madhur/github/ASTopology/Aggregation.htm"
page = open(url)
soup = BeautifulSoup(page.read())
print soup