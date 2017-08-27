#!/usr/bin/python3.5

import os, sys

if(len(sys.argv)<3):
	print("Usage: ./{} [IP ADDRESS] [PORT OID]".format(sys.argv[0]))
	exit(3)
status = os.popen("/usr/bin/snmpget -v1 -c public -Cf {} {} | sed 's/.*INTEGER: //'".format(sys.argv[1], sys.argv[2]))
status = int(status.read())

oid = sys.argv[2].split(".")
oid[9] = '2'
oid = ".".join(oid)

name = os.popen("/usr/bin/snmpget -v1 -c public -Cf {} {} | sed 's/.*STRING: //'".format(sys.argv[1], oid))
name = name.read()

p,r = "",3
if status == 2:
	p,r = "DOWN",2
elif status == 1:
	p,r = "UP",0

print("{} status is {};".format(name[:-1], p))
exit(r)
