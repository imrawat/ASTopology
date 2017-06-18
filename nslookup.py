import os
import time
import constants
import commands


in_file = constants.TEST_DATA + "IN/IN_govt.txt"


with open(in_file) as fi:
	for line in fi:
		line = line.strip()
		if not line[0] == "#":
			splits = line.split()
			# if splits[0][:3] == "www":
			# 	command = "nslookup "+ splits[0]
			# else:
			# 	command = "nslookup www." + splits[0]
			# print line
			# os.system(command)
			if len(splits) > 1:
				command = "whois -h whois.cymru.com \" -v " + splits[1] + "\""
				result = commands.getoutput(command)
				asline = result.split("\n")[1]
				aslinesplits =  asline.split("|")
				AS = aslinesplits[0].strip()
				bgp_prefix = aslinesplits[2].strip()
				print splits[0], splits[1], AS, bgp_prefix
			
			# command = "dig " + splits[0] + " 8.8.8.8 +short"
			# result = commands.getoutput(command)
			# print splits[0], result

			time.sleep(3)