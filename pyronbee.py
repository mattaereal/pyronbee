#!/usr/bin/env python
# -*- coding: latin-1 -*-

# Copyright (c) <2012> Matías Ariel Ré Medina <mre@infobytesec.com> 

# pyronbee is my humble implementation of the idea represented on the tool made
# by ivanr from Qualys, in perl, called waf-research.

# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from httplib2 import HTTPConnectionWithTimeout as HTTPCustom
from json import load as JSONLoad
from urllib import urlencode
import sys

class PyronBee:

	def __init__(self, host, port, files, timeout=10):
		"""
		Just the initialization.
		
		"""
		self.host = host
		self.port = port
		self.test_files = files
		self.timeout = timeout

		self.startTests()


	def startTests(self):
		"""
		Loops gathering data from input files and then uses them on a request.
		"""
		while (self.test_files):
			http = HTTPCustom(self.host, self.port, self.timeout)
			request = self.readRequestFromJSON()
			self.makeRequest(http, request)
			response = self.getResponse(http, request)
			self.output(self.currentFilename, response)


	def getResponse(self, http, req):
		"""
		Returns an http response object.
		
		"""
		return http.getresponse()

	def makeRequest(self, http, req):
		"""
		Makes an http request using certain keys from req dictionary.
		
		"""
		params = urlencode(req["body"]) # For post data.
		http.request(req["method"], req["url"], params, req["headers"])

	def readRequestFromJSON(self):
		"""
		Reads the request data stored in the file with JSON syntax.
		"""
		self.currentFilename = self.test_files.pop()
		try:
			currentFile = open(self.currentFilename)
			data = JSONLoad(currentFile)
			currentFile.close()
			return data
		except:
			print "No JSON object could be decoded - %s" % self.currentFilename
			if self.test_files:
				return self.readRequestFromJSON()
			sys.exit(2)

	def output(self, filename, response):
		"""
		Prints how the test went.
		"""
		print self.translateStatusCode(response), "["+filename+"]"

	def translateStatusCode(self, response):
		"""
		Returns a human readable representation of the result status of the 
		current test.

		"""
		if response.status != 200:
			return "[+] Blocked"
		else:
			return "[!] Missed"


if __name__ == "__main__":
    sys.stderr.write("# Copyright (c) <2012> <Matías Ariel Ré Medina>\n")
    sys.stderr.write("# pyronbee, idea from ivanr's waf-research\n")

    if len(sys.argv) >= 4:
    	pb = PyronBee(sys.argv[1], sys.argv[2], sys.argv[3:])

    else:
        print "[!] Usage: %s host port test_files" % sys.argv[0]
        print "[!] Examples:"
        print "\t %s mfsec.com.ar 80 request.test" % sys.argv[0]
        print "\t %s mfsec.com.ar 443 *.test" % sys.argv[0]
        sys.exit(2)