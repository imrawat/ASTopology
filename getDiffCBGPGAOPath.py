COUNTRY_CODE='EG'

C2C_PATHFILE=COUNTRY_CODE+'2'+COUNTRY_CODE+'_finalpaths.txt'
CBGP_C2C_PATHFILE='cbgp'+C2C_PATHFILE
C2C_PATHFILE='./'+C2C_PATHFILE
CBGP_C2C_PATHFILE='./'+CBGP_C2C_PATHFILE

# C2C_PATHFILE='./EG2EG_finalpaths2.txt'
# CBGP_C2C_PATHFILE='./cbgpEG2EG_finalpaths2.txt'

print
print 'gao c2c path '+C2C_PATHFILE
print 'cbgp c2c path' +CBGP_C2C_PATHFILE
print

gao_path_dict=dict()
gao_path_hopcount_dict=dict()
cbgp_path_dict=dict()

with open(C2C_PATHFILE) as fi:
        for line in fi:
		ll=line.strip()
		splits=ll.split(' ')
                prefix=splits[0]
                startAS=splits[len(splits)-1]
                key=prefix+':'+startAS
                gao_path_dict[key]=ll
                gao_path_hopcount_dict[key]=len(splits)-1

diff_hopcount=0
notin_gaopath=0
notin_cbgppath=0
same_path=0

with open(CBGP_C2C_PATHFILE) as fi:
	for line in fi:
		ll=line.strip()
		splits=ll.split(' ')
                prefix=splits[0]
                startAS=splits[len(splits)-1]
                key=prefix+':'+startAS
                cbgp_path_dict[key]=ll
                if key in gao_path_hopcount_dict:
                	if gao_path_hopcount_dict[key]==(len(splits)-1):
                                if gao_path_dict[key]==ll:
                                        same_path=same_path+1
                	else:
                                diff_hopcount=diff_hopcount+1

                else:
                        notin_gaopath=notin_gaopath+1

with open(C2C_PATHFILE) as fi:
        for line in fi:
                ll=line.strip()
                splits=ll.split(' ')
                prefix=splits[0]
                startAS=splits[len(splits)-1]
                key=prefix+':'+startAS
                if not key in cbgp_path_dict:
                        notin_cbgppath=notin_cbgppath+1

print 'startAS prefix pair in gao '+str(len(gao_path_dict))
print 'startAS prefix pair in cbgp '+str(len(cbgp_path_dict))
print 'diff_hopcount '+str(diff_hopcount)
print 'cbgp path not in gao path '+str(notin_gaopath)
print 'gao path not in cbgp path '+str(notin_cbgppath)
print 'same_path '+str(same_path)

