import os
import time

with open("CN_govt.txt") as fi:
	for line in fi:
		line = line.strip()
		splits = line.split()
		command = "nslookup www."+ split[0]
		time.sleep(2)
		print command
		os.system(command)