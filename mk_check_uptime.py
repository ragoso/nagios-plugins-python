#!/usr/bin/python3.5

import os, sys, re


if(len(sys.argv)<4):
	print("Usage: ./{} [IP ADDRESS] [W] [C]".format(sys.argv[0]))
	exit(3)

f = os.popen("/usr/bin/snmpget -v1 -c public -Cf {} 1.3.6.1.2.1.1.3.0".format(sys.argv[1]))
line = f.read()

days = re.findall(r'[0-9]* (?=day)', line)
hours = re.findall(r'[0-9]{0,2}:[0-9]{0,2}:[0-9]{0,2}', line)

if(len(days)>0):
	days = int(days[0])
else:
	days = 0
#hours = hours[0].split(':')


p = 3
if days == int(sys.argv[3]):
	r  = 2
elif days > int(sys.argv[3]) and days <= int(sys.argv[2]):
	r = 1
else:
	r = 0

print("Uptime is {} days {} hours".format(days, hours[0]))
exit(r)
