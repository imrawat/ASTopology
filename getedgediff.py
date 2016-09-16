# gives edge difference between intermediate AS's of two different pathset files.

import urllib
import urllib2
import requests
import os
import sys

f1=sys.argv[1]
f2=sys.argv[2]

f1_path='./1to'+f1+'.txt'
f2_path='./1to'+f2+'.txt'

f1_path='./finalpaths_1_to_100.txt'
f2_path='./finalpaths_100_to_200.txt'

f1_set = set()
repeated_f1=0
unique_f1=0
f2_set = set()
repeated_f2=0
unique_f2=0

with open(f1_path) as f1o:
	paths_f1 = f1o.readlines()

with open(f2_path) as f2o:
	paths_f2 = f2o.readlines()

for path_f1 in paths_f1:
	path_f1=path_f1.rstrip()
	split = path_f1.split(' ')
	as1 = ' '
	as2 = ' '
	count = 0
	for asno in split[5:len(split)-1]:
		count = count +1
		if count==1:
			as1=asno
		elif count==2:
			as2=asno
			key=' '
			if int(as1)<int(as2):
				key=as1+':'+as2
			else:
				key=as2+':'+as1
			if not key in f1_set:
				f1_set.add(key)
				unique_f1 = unique_f1+1
			else:
				repeated_f1=repeated_f1+1
			as1=as2
			count = 1

#iterate file2 paths and find edges in f1 set prepared above
notfound_set = set()
notfound_count=0
for path_f2 in paths_f2:
	path_f2=path_f2.rstrip()
        split = path_f2.split(' ')
        as1 = ' '
        as2 = ' '
        count = 0
        for asno in split[5:len(split)-1]:
                count = count +1
                if count==1:
                        as1=asno
                elif count==2:
                        as2=asno
                        key=' '
                        if int(as1)<int(as2):
                                key=as1+':'+as2
                        else:
                                key=as2+':'+as1
			if not key in f1_set and not key in notfound_set:
				notfound_count=notfound_count+1
				notfound_set.add(key)

			if not key in f2_set:
                                f2_set.add(key)
                                unique_f2 = unique_f2+1
                        else:
                                repeated_f2=repeated_f2+1
			as1=as2
                        count = 1


print 'unique edges in '+f1_path+' : '+str(unique_f1)
print 'repeated edges in '+f1_path+' : '+str(repeated_f1)
print ' '
print 'unique edges in '+f2_path+' : '+str(unique_f2)
print 'repeated edges in '+f2_path+' : '+str(repeated_f2)
print ' '
print f2_path+' edges not in '+f1_path+' : '+str(notfound_count)
