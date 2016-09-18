import os

with open('./prefixlist.txt') as f:
	prefixes = f.readlines()
pref = 'screen -d -m java -jar Facebook.jar '
for prefix in prefixes[0:4]:
	pp = prefix[0:len(prefix)-2]
	command = pref+pp
	print pp
	os.system(command)
