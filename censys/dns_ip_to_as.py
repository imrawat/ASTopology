'''
Convert dns resolver ip's to their respective as numbers and 
save them along with other cymuru metadata information
'''
import os
import time
import argparse
import subprocess
import commands
import time
import sys
import math
import fcntl

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = 'get AS for dns resolver IP')
	parser.add_argument('-c', '--country_code', help='DNS resolver ip to as mapping', required = True)
	parser.add_argument('-ls', '--line_to_start_from', help='from where to start in dns ip file. will append \
		output if argument is provided', required = False)
	parser.add_argument('-le', '--line_to_end', help='from where to end in dns ip file. will append \
		output if argument is provided', required = False)

	args = parser.parse_args()
	COUNTRY_CODE = args.country_code
	START_LINE_NUMBER = args.line_to_start_from
	END_LINE_NUMBER = args.line_to_end

	# if (START_LINE_NUMBER == None and not END_LINE_NUMBER == None) or (not START_LINE_NUMBER == None andw END_LINE_NUMBER == None:):
	# 	print "Provide both start and end line number"
	# 	exit()

	in_file = "dns_resolvers_" + COUNTRY_CODE + ".csv"
	print "in_file " + in_file

	out_file = "dns_resolvers_ip_to_as_" + COUNTRY_CODE + ".csv"
	print "out_file " + out_file

	error_file = "dns_resolvers_ip_to_as_error_" + COUNTRY_CODE + ".csv"
	print "error_file " + error_file

	HEADER = "ip,location_country,location_city,location_province,p53_dns_lookup_resolves_correctly,"
	HEADER = HEADER + "p53_dns_lookup_open_resolver,p53_dns_lookup_support,AS,BGP Prefix,CC,AS Name\n"

	if START_LINE_NUMBER == None:
		print "Rewriting output file"
		START_LINE_NUMBER = 1
		OP_MODE = "w"
		fo = open(out_file, OP_MODE)
		fo.write(HEADER)
		fe = open(error_file, OP_MODE)
	elif START_LINE_NUMBER.isdigit() and int(START_LINE_NUMBER) > 0:
		START_LINE_NUMBER = int(START_LINE_NUMBER)
		OP_MODE = "a"
		fo = open(out_file, OP_MODE)
		fe = open(error_file, OP_MODE)
	else:
		print "Invalid start line number provided"
		exit()

	if END_LINE_NUMBER == None:
		END_LINE_NUMBER = float('inf')
	elif END_LINE_NUMBER.isdigit() and int(END_LINE_NUMBER) >= START_LINE_NUMBER:
		END_LINE_NUMBER = int(END_LINE_NUMBER)
	else:
		print "Invalid end line number provided"
		exit()
	print START_LINE_NUMBER, END_LINE_NUMBER

	with open(in_file) as fi:
		curr_line = 0
		for line in fi:
			curr_line = curr_line + 1
			if curr_line >= START_LINE_NUMBER and curr_line > 1 and curr_line <= END_LINE_NUMBER:
				line = line.strip()
				splits = line.split(",")
				ip = splits[0]
				location_country = splits[1]
				location_city = splits[2]
				location_province = splits[3]
				p53_dns_lookup_resolves_correctly = splits[4]
				p53_dns_lookup_open_resolver = splits[5]
				p53_dns_lookup_support = splits[6]

				command = "whois -h whois.cymru.com \" -v " + ip + "\""
				# result = subprocess.check_output(command, shell=True)
				result = commands.getoutput(command)
				print result
				print curr_line, command
				try:
					asline = result.split("\n")[1]
					aslinesplits =  asline.split("|")
					AS = aslinesplits[0].strip()
					bgp_prefix = aslinesplits[2].strip()
					cc = aslinesplits[3].strip()
					as_name = aslinesplits[6].strip()
					line_to_write = ip + "," + location_country + "," + location_city + "," + location_province + "," 
					line_to_write = line_to_write + p53_dns_lookup_resolves_correctly + "," + p53_dns_lookup_open_resolver 
					line_to_write = line_to_write + "," + p53_dns_lookup_support + "," + AS + "," + bgp_prefix + "," + cc 
					line_to_write = line_to_write + "," + as_name
					if OP_MODE == "a":
						fcntl.flock(g, fcntl.LOCK_EX)
						fo.write(line_to_write + "\n")
						fcntl.flock(g, fcntl.LOCK_UN)
					elif OP_MODE == "w":
						fo.write(line_to_write + "\n")
					time.sleep(1)
				except:
					fe.write(str(curr_line) + " " + command + "\n")
					fe.write(str(sys.exc_info()[0]) + "\n\n")


