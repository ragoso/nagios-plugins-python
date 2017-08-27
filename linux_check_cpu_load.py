#!/usr/bin/python3.5

import os, sys

if(len(sys.argv)<4):
	print("Usage: ./{} [IP ADDRESS] [W] [C]".format(sys.argv[0]))
	exit(3)
f = os.popen("/usr/bin/snmpget -v1 -c public -Cf {} 1.3.6.1.4.1.2021.10.1.3.1 | sed 's/.*STRING: //'".format(sys.argv[1]))
load = float(f.read()[1:-2])

if load >= float(sys.argv[2]) and load < float(sys.argv[3]):
	r = 1
elif load >= float(sys.argv[3]):
	r = 2
else:
	r = 0

print("CPU Load is {}%;".format(load))
exit(r)
