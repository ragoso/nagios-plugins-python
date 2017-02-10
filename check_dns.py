#!/usr/bin/python

## pip install dnspython

import dns.resolver

resolver = dns.resolver.Resolver()
resolver.nameservers = ['168.121.40.3']

answer = resolver.query('google.com')

print(answer.rrset)
