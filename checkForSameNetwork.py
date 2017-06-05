import constants

INFILE = constants.TEST_DATA + "IN_ASPrefixes.txt"
# AS35553 192.115.240.0/22

IS_IMP_AS = False
print "IS_IMP_AS " + str(IS_IMP_AS)
print

networkdict = dict()
with open(INFILE) as fi:
	for line in fi:
		line = line.strip()
		
		if not line[0] == "#":
			splits = line.split()
			if IS_IMP_AS:
				AS = splits[2]
				ip = splits[1]
				mask = 32
			else:
				AS = splits[0]
				prefix = splits[1]
				prefsplits = prefix.split("/")
				if len(prefsplits) < 2:
					print line + " len(prefsplits) " + str(len(prefsplits)) 
					continue
				mask = prefsplits[1]
				mask = int(mask)
				ip = prefsplits[0]
			ipsplits = ip.split(".")
			if len(ipsplits) < 4:
				print line + " len(ipsplits) " + str(len(ipsplits)) 
				continue
			network = ""
			for d in ipsplits:
				b = bin(int(d))
				b = b[2:]
				while(len(b) < 8):
					b = "0" + b
				network = network + b
			network = network[:mask]
			if network in networkdict:
				networkdict[network].append(AS)
			else:
				ASlist = [AS]
				networkdict[network] = ASlist

fi.close()
for network in networkdict:
	print network, networkdict[network]
