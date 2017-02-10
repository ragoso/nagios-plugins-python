#!/usr/bin/python
import sys
import pycurl
import cStringIO
import re

if len(sys.argv) < 2 :
	print 'Usage: %s [url]' % __file__
	sys.exit()

c = pycurl.Curl()

buffer = cStringIO.StringIO()
header = cStringIO.StringIO()

c.setopt(pycurl.URL, sys.argv[1])
c.setopt(pycurl.WRITEFUNCTION, buffer.write)
c.setopt(pycurl.HEADERFUNCTION, header.write)
c.perform()

status_line = header.getvalue().splitlines()[0]
m = re.match(r'HTTP\/\S*\s*\d+\s*(.*?)\s*$', status_line)

if m:
	status_msg = m.groups(1)
else:
	status_message = ''


print 'STATUS %s %s, %f ms' % (c.getinfo(pycurl.HTTP_CODE), status_msg[0], c.getinfo(pycurl.TOTAL_TIME))
