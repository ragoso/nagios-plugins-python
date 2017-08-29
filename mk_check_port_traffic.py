#!/usr/bin/python3.5

import os, sys, time

if(len(sys.argv)<7):
	print("Usage: ./{} [IP ADDRESS] [PORT OID SUFFIX] [W IN] [C IN] [W OUT] [C OUT]".format(sys.argv[0]))
	exit(3)

oid_prefix = "1.3.6.1.2.1.31.1.1.1."
oid_bytes_in = oid_prefix + "6." + sys.argv[2]
oid_bytes_out = oid_prefix + "10." + sys.argv[2]


bytes_in = os.popen("/usr/bin/snmpget -v1 -c public -Cf {} {} | sed 's/.*Counter64: //'".format(sys.argv[1], oid_bytes_in))
time1_in = time.time()
time.sleep(1)

bytes_in2 = os.popen("/usr/bin/snmpget -v1 -c public -Cf {} {} | sed 's/.*Counter64: //'".format(sys.argv[1], oid_bytes_in))
time2_in = time.time()

bytes_in = int(bytes_in.read())
bytes_in2 = int(bytes_in2.read())

bytes_in_sec = (bytes_in2 - bytes_in) / (time2_in - time1_in)
kbits_in = (bytes_in_sec / 1024) * 8

bytes_out = os.popen("/usr/bin/snmpget -v1 -c public -Cf {} {} | sed 's/.*Counter64: //'".format(sys.argv[1], oid_bytes_out))
time1_out = time.time()
time.sleep(1)
bytes_out2 = os.popen("/usr/bin/snmpget -v1 -c public -Cf {} {} | sed 's/.*Counter64: //'".format(sys.argv[1], oid_bytes_out))
time2_out = time.time()

bytes_out = int(bytes_out.read())
bytes_out2 = int(bytes_out2.read())
bytes_out_sec = (bytes_out2 - bytes_out) / (time2_out - time1_out)
kbits_out = (bytes_out_sec / 1024) * 8

oid_name = oid_bytes_in.split(".")
oid_name[6] = '2'
oid_name[7] = '2'
oid_name[9] = '2'
oid_name[10] = sys.argv[2]
oid_name = ".".join(oid_name)
oid_name = oid_name[:-2]

name = os.popen("/usr/bin/snmpget -v1 -c public -Cf {} {} | sed 's/.*STRING: //'".format(sys.argv[1], oid_name))
name = name.read()


if (kbits_in < float(sys.argv[3]) or kbits_out < float(sys.argv[5])) and  (kbits_in > float(sys.argv[4]) and kbits_out > float(sys.argv[6])):
	r = 2
elif (kbits_in < float(sys.argv[4]) or kbits_out < float(sys.argv[6])):
	r = 1
else:
	r = 0


if kbits_out > 1000:
        kbits_out = kbits_out / 1000
        out =  "Mbps"
else:
        out = "Kbps"

if kbits_in > 1000:
        kbits_in = kbits_in / 1000
        iin = "Mbps"
else:
        iin = "Kbps"


print("{} interface traffic is: Out {:.1f} {} / In {:.1f} {}".format(name[1:-2], kbits_out, out, kbits_in, iin))
exit(r)
