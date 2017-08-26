import os, sys

if(len(sys.argv)<4):
	print("Usage: ./{} [IP ADDRESS] [W] [C]".format(sys.argv[0]))
	exit(3)
f = os.popen("/usr/bin/snmpget -v1 -c public -Cf {} 1.3.6.1.2.1.25.3.3.1.2.1 | sed 's/.*INTEGER: //'".format(sys.argv[1]))
load = int(f.read())
p,r = "",3
if load >= int(sys.argv[2]) and load < int(sys.argv[3]):
	p,r = "WARNING",1

elif load >= int(sys.argv[3]):
	p,r = "CRITICAL",2
else:
	p,r = "OK",0

print("{} - CPU Load is {}%;".format(p, load))
exit(r)