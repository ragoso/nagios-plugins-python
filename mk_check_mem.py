#!/usr/bin/python3.5

import os, sys

if(len(sys.argv)<4):
	print("Usage: ./{} [IP ADDRESS] [W] [C]".format(sys.argv[0]))
	exit(3)
total = os.popen("/usr/bin/snmpget -v1 -c public -Cf {} 1.3.6.1.2.1.25.2.3.1.5.65536 | sed 's/.*INTEGER: //'".format(sys.argv[1]))
total = int(total.read())

used = os.popen("/usr/bin/snmpget -v1 -c public -Cf {} 1.3.6.1.2.1.25.2.3.1.6.65536 | sed 's/.*INTEGER: //'".format(sys.argv[1]))
used = int(used.read())

used = (used * 100) / total

p = 3
if used >= int(sys.argv[3]):
	r  = 2
elif used < int(sys.argv[3]) and used >= int(sys.argv[2]):
	r = 1
else:
	r = 0

print("RAM Used is %.2f" % used, "%")
exit(r)
