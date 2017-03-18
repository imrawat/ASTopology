import os
import time

with open("CN_govt.txt") as fi:
	for line in fi:
		line = line.strip()
		splits = line.split()
		ip = splits[1]
		# whois -h whois.cymru.com " -v 103.9.85.40"
		command = "whois -h whois.cymru.com \" -v "+ ip + "\""
		time.sleep(2)
		print
		print splits[0]
		print command
		os.system(command)