import urllib
import urllib2
import requests
import os
import sys

upto=sys.argv[1]

out_path='./1to'+upto+'.txt'
fout=open(out_path, 'w')

with open("./top100prefixes.txt") as f1:
	prefixes = f1.readlines()

#finalpaths_1_to_100.txt
with open("./finalpaths_1_to_100.txt") as f2:
        paths = f2.readlines()

count = 0;
for prefix in prefixes:
	prefix=prefix.rstrip();
	count = count+1;
	found=0;
	for path in paths:
		path=path.rstrip();
		path_prefix=path.split(' ')[0]
		if prefix==path_prefix:
			if(found==0):
				found=1
				print 'writing '+prefix+' to '+out_path
			fout.write(path+'\n')
	if str(count)==upto:
		break
