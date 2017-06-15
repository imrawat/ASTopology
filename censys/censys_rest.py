# !/usr/bin/env python
# Name :  Madhur Rawat
# Date : 09/06/17

import argparse
import json
import requests
import codecs
import locale
import os
import sys
import ast
import time

class Censys:
	def __init__(self, country_code):
		self.API_URL = "https://www.censys.io/api/v1"
		self.UID = "b4cb5219-9016-473a-a111-9d60aff15f46"
		self.SECRET = "nh2p3Lpyz4J07E4kKCRmJKKHbZonkXtC"
		self.country_code = country_code

	def search(self, page, pages):
		out_file = "dns_resolvers_" + self.country_code
		fo = open(out_file, "w")
		while (page <= pages):  
			# location.country_code: DE and protocols: ("53/dns")
			data = {
				"query" : "location.country_code: " + self.country_code + " and protocols: (\"53/dns\")",
				# "fields" :
				# 	[
				# 		"ip",
				# 		"location.country",
				# 		"protocols"
				# 	],
				"page" : page
			}
			# params = {data, 'page' : page}
			# res = requests.post(self.API_URL + "/search/ipv4", json = params, auth = (self.UID, self.SECRET))
			res = requests.post(self.API_URL + "/search/ipv4", data=json.dumps(data), auth = (self.UID, self.SECRET))
			payload = res.json()
			print payload
			for r in payload['results']:
				# print (r["ip"], r["protocols"], r["location.country"])
				print (r)
				fo.write(str(r["ip"]) + " " + str(r["protocols"]) + " " + str(r["location.country"]) + "\n")
			print (page)
			time.sleep(3)
			pages = payload['metadata']['pages']
			page = page + 1
		fo.close()


parser = argparse.ArgumentParser(description = 'CENSYS.IO DNS resolver search')
parser.add_argument('-c', '--country_code', help='CENSYS Search', required = True)
parser.add_argument('-p', '--page_number', help='CENSYS Search', required = False)
pages = float("inf")
page = 1
args = parser.parse_args()
country_code = args.country_code
# if args.page_number != None:
# 	page = args.page_number
 
censys = Censys(country_code)
censys.search(page, pages)
