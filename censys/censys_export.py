# !/usr/bin/env python
# Name :  Madhur Rawat
# Date : 17/06/17

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
		self.UID = "bff072bf-ba2c-40e1-ad3c-10db1b4fe3df"
		self.SECRET = "rUmUaZtFIFC94k5AGJVydINOsgizA7oP"
		self.country_code = country_code

	def export(self):
		data = {
			"query":"SELECT location.country, count(ip) FROM ipv4.20151020 GROUP BY location.country;",
			"format":"json",
			"flatten":"false"
		}
		res = requests.post(self.API_URL + "/export", data=json.dumps(data), auth = (self.UID, self.SECRET))
		payload = res.json()
		print payload
		


parser = argparse.ArgumentParser(description = 'CENSYS.IO export module')
parser.add_argument('-c', '--country_code', help='CENSYS Export', required = True)

pages = float("inf")
page = 1
args = parser.parse_args()
country_code = args.country_code
censys = Censys(country_code)
censys.export()
