# Get path from finalpaths.txt
# Path from an AS within Egypt to Egypt Prefix.
# Such an AS can be start or intermediatry AS.

EGAS_set=set()
with open("./EgyptASwoRank.txt") as fi:
        for line in fi:
                AS=line[2:len(line)-1]
                if not AS in EGAS_set:
                        EGAS_set.add(AS)


fo=open('./EG2EG_finalpaths.txt', 'w')
with open("./finalpaths.txt") as f2:
        for line in f2:
                ll=line[:len(line)-1]
                splits=ll.split(' ')
		ASidx=len(splits)-1
                for AS in splits[len(splits):4:-1]:
			if AS in EGAS_set and AS!=splits[3]:
				idx=0
				line_to_write=''
				for sp in splits:
					if idx>ASidx: #check if path is written upto found AS.
						line_to_write=line_to_write[:len(line_to_write)-1]
						break #write only uptil index of found AS
					if idx!=1 and idx!=2 and idx!=3:
						line_to_write=line_to_write+sp+' '
					idx=idx+1
				fo.write(line_to_write+'\n')
				print ll+' : '+AS
				print line_to_write
				break # An AS found. Continue to next path now.
			ASidx=ASidx-1 #decrement AS index from right

fo.close()