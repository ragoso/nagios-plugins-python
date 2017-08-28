#!/usr/bin/python3.5

import os, sys

if(len(sys.argv)<3):
	print("Usage: ./{} [IP ADDRESS] [PORT OID]".format(sys.argv[0]))
	exit(3)

oid_prefix = "1.3.6.1.2.1.2.2.1.8."
oid_status = oid_prefix + sys.argv[2]
status = os.popen("/usr/bin/snmpget -v1 -c public -Cf {} {} | sed 's/.*INTEGER: //'".format(sys.argv[1], oid_status))
status = int(status.read())

oid_name = oid_status.split(".")
oid_name[9] = '2'
oid_name = ".".join(oid_name)

name = os.popen("/usr/bin/snmpget -v1 -c public -Cf {} {} | sed 's/.*STRING: //'".format(sys.argv[1], oid_name))
name = name.read()

p,r = "",3
if status == 2:
	p,r = "DOWN",2
elif status == 1:
	p,r = "UP",0

print("{} status is {};".format(name[:-1], p))
exit(r)
