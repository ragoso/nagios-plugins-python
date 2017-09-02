#!/usr/bin/python3.5

import os, sys

if(len(sys.argv)<4):
	print("Usage: ./{} [IP ADDRESS] [W] [C]".format(sys.argv[0]))
	exit(3)
total = os.popen("/usr/bin/snmpget -v1 -c public -Cf {} 1.3.6.1.4.1.2021.9.1.9.1 | sed 's/.*INTEGER: //'".format(sys.argv[1]))
total = int(total.read())


if total >= int(sys.argv[2]) and total < int(sys.argv[3]):
	r = 2
elif total >= int(sys.argv[3]):
	r = 1
else:
	r = 0


print("Disk Usage is {}%".format(total))
exit(r)
