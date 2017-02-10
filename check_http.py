#!/usr/bin/python
import sys
import urllib

req = urllib.urlopen(sys.argv[1])
print(req.getcode())
