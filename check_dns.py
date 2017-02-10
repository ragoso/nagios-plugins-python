#!/usr/bin/python

## pip install dnspython

import sys
import dns.resolver

import time
if len(sys.argv) < 3:
	print 'Usage: %s [server ip] [domain]' % __file__
	sys.exit()


resolver = dns.resolver.Resolver()
resolver.nameservers = [sys.argv[1]]

start_time = time.time()
answer = resolver.query(sys.argv[2])
end_time = time.time()
print('%s,  %s ms' % (answer.rrset, end_time - start_time))
