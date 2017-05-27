import os
import time

with open("CN_govt.txt") as fi:
	for line in fi:
		line = line.strip()
		if not line[0] == "#":
			splits = line.split()
			if splits[0][:3] == "www":
				command = "nslookup "+ splits[0]
			else:
				command = "nslookup www." + splits[0]
			print line
			# if len(splits) > 1:
			# 	command = "whois -h whois.cymru.com \" -v " + splits[1] + "\""

			time.sleep(1.5)
			
			print command
			os.system(command)
			print
			print 50*('*')