#!/usr/bin/python

## pip install dnspython

import dns.resolver

resolver = dns.resolver.Resolver()
resolver.nameservers = ['8.8.8.8']

answer = resolver.query('google.com')

print(answer.rrset)
