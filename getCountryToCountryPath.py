# Get path from finalpaths.txt
# Path from an AS within Egypt to Egypt Prefix.
# Such an AS can be start or intermediatry AS.
from collections import OrderedDict

IS_CAIDA = True
if IS_CAIDA:
	print "*** CAIDA is Enabled ***"

COUNTRY_CODE='EG'

COUNTRY_AS_LIST='./'+COUNTRY_CODE+'_AS.txt'
print 'COUNTRY_AS_LIST : '+COUNTRY_AS_LIST

PATH_FILE='./finalpaths.txt'
if IS_CAIDA:
	PATH_FILE='./'+COUNTRY_CODE+'_gao_cbgp_paths.txt'
print 'PATH_FILE : '+PATH_FILE


OUT_FILE=COUNTRY_CODE+'2'+COUNTRY_CODE+'_finalpaths.txt'
if IS_CAIDA:
	OUT_FILE='cbgp'+OUT_FILE
OUT_FILE='./'+OUT_FILE
print 'OUT_FILE : '+OUT_FILE

print 

EGAS_set=set()
with open(COUNTRY_AS_LIST) as fi:
        for line in fi:
                AS=line[2:len(line)-1]
                if not AS in EGAS_set:
                        EGAS_set.add(AS)

fo=open(OUT_FILE, 'w')

with open(PATH_FILE) as f2:
    for line in f2:
            ll=line[:len(line)-1]
            splits=ll.split(' ')
            ASidx=len(splits)-1
            homeProviderIdx=5
            if IS_CAIDA:
            	homeProviderIdx=2

            # set of AS found in current path.
            ASFoundInCurrentPath=set()
            for AS in splits[len(splits):homeProviderIdx-1:-1]:
				homeIdx=4
				if IS_CAIDA:
					homeIdx=1
				if AS in EGAS_set and AS!=splits[homeIdx] and not AS in ASFoundInCurrentPath:
					idx=0
					line_to_write=''
					temp_dict=OrderedDict()
					ASFoundInCurrentPath.add(AS)
					for sp in splits:
						#check if path is written upto found AS.
						if idx>ASidx: 
							for key in temp_dict:
								line_to_write=line_to_write+' '+key
							line_to_write=line_to_write[1:]
							#write only uptil index of found AS
							break 
						if not IS_CAIDA:
							if idx!=1 and idx!=2 and idx!=3:
								if not sp in temp_dict:
									temp_dict[sp]=1
						else:
							if not sp in temp_dict:
									temp_dict[sp]=1
						idx=idx+1
					fo.write(line_to_write+'\n')
					print ll+' : '+AS
					print line_to_write
#				break # An AS found. Continue to next path now.
				ASidx=ASidx-1 #decrement AS index from right

fo.close()
