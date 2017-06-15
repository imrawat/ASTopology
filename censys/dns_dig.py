import os
import time
import argparse
import subprocess
import commands
import time

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = 'get dig response for dns ip\'s')
	parser.add_argument('-c', '--country_code', help='country_code of dns resolver file', required = True)
	parser.add_argument('-l', '--line_to_start_from', help='from where to start in dns ip file. will append \
		output if argument is provided', required = False)

	args = parser.parse_args()
	COUNTRY_CODE = args.country_code
	LINE_NUMBER = args.line_to_start_from

	in_file = "dns_resolvers_" + COUNTRY_CODE + ".csv"
	in_file = "opendns.txt"
	print "in_file " + in_file

	out_file = "dns_resolvers_dig_" + COUNTRY_CODE + ".csv"
	print "out_file " + out_file

	if LINE_NUMBER == None:
		print "Rewriting output file"
		LINE_NUMBER = 1
		OP_MODE = "w"
		fo = open(out_file, OP_MODE)
	elif LINE_NUMBER.isdigit() and int(LINE_NUMBER) > 0:
		LINE_NUMBER = int(LINE_NUMBER) + 1
		OP_MODE = "a"
		fo = open(out_file, OP_MODE)
	else:
		print "Invalid line number provided"
		exit()

	with open(in_file) as fi:
		curr_line = 0
		for line in fi:
			curr_line = curr_line + 1
			if curr_line >= LINE_NUMBER and curr_line > 1:
				line = line.strip()
				splits = line.split(",")
				ip = splits[0]
				command = "dig @" + ip + " www.google.com +short"
				# result = subprocess.check_output(command, shell=True)
				result = commands.getoutput(command)
				print command
				print line
				# SEPARATOR = "************************************************"
				if len(result) > 0 and len(result) < 35:
					fo.write(ip + " " + result + "\n")
					print "answer ", result
					print
				# fo.write(SEPARATOR)
				time.sleep(1)
		fo.close()
