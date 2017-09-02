#!/usr/bin/python3.5

import os, sys

if(len(sys.argv)<4):
	print("Usage: ./{} [IP ADDRESS] [W] [C]".format(sys.argv[0]))
	exit(3)
total = os.popen("/usr/bin/snmpget -v1 -c public -Cf {} 1.3.6.1.4.1.2021.4.5.0 | sed 's/.*INTEGER: //'".format(sys.argv[1]))
total = int(total.read())

avaliable = os.popen("/usr/bin/snmpget -v1 -c public -Cf {} 1.3.6.1.4.1.2021.4.11.0 | sed 's/.*INTEGER: //'".format(sys.argv[1]))
avaliable = int(avaliable.read())
free = (avaliable * 100) / total
used = 100 - free

if free <= int(sys.argv[2]) and free > int(sys.argv[3]):
	r = 2
elif free <= int(sys.argv[3]):
	r = 1
else:
	r = 0


print("RAM Used is %.2f" % used, "%")
exit(r)
