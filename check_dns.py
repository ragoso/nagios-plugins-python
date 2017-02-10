#!/usr/bin/python

## pip install dnspython

import sys
import dns.resolver

resolver = dns.resolver.Resolver()
resolver.nameservers = [sys.argv[1]]

answer = resolver.query(sys.argv[2])

print(answer.rrset)
