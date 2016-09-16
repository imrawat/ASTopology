import bz2
import sys
import os

from os.path import basename

folder='./'+sys.argv[1]

folderstart=sys.argv[1]
folderend=sys.argv[2]


print "decompressing file for folder from "+str(folderstart)+" to "+str(folderend)

for folder in range(int(folderstart), (int(folderend)+1)):
	folder_path='./'+str(folder)
	for file in os.listdir(folder_path):
		if file.endswith(".bz2"):
	        	print file
        	#if(sys.argv[1]=='8' and (file=='RIB07.bz2' or file=='RIB08.bz2')):
                #	print 'skipping..'
                #	continue;
        		file_no_ext =  os.path.splitext(file)[0]
	        	file_path=folder_path+'/'+file
        		save_path=folder_path+'/'+file_no_ext+'.bin'
        		f = open(file_path, 'r')
        		data=f.read()
        		out=bz2.decompress(data)
        		fo = open(save_path,'w')
        		fo.write(out)
