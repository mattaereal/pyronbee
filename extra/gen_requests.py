#!/usr/bin/env python

# pyronbee test file requests generator.
# Just a simple tool to automatize certain requests with certain URL.

import sys, json

if len(sys.argv) == 4:
	fp = open(sys.argv[2])
	url = sys.argv[1]
	prefix = sys.argv[3]

	request = { "method": "GET", "url": "/", "http_ver": "HTTP/1.1", "urlencoded": None, "multipart" : None, "headers":  {"User-Agent": "pyronbee", "Connection": "Close" }, "description": "No description", "status_codes": [200] }
	i = 1
	filename = prefix
	for line in fp:
		request["url"] = url + line.strip()
		cf = filename + str(hex(i)) + ".test"
		cfp = open(cf, "a")
		cfp.write(json.dumps(request))
		cfp.close()
		i += 1

else:
	print "Usage: %s URL REQUESTS_FILE PREFIX" % sys.argv[0]
	print "Example:"
	print "\t%s /index.php?search= requests isr_example_" % sys.argv[0]