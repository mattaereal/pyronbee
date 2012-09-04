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

import sys
from CustomHTTPLib import CustomHTTPLib
from json import load as JSONLoad

class PyronBee:

	def __init__(self, host, port, files, timeout=10):
		"""
		Just the initialization.
		
		"""
		self.host = host
		self.port = port
		self.test_files = files
		self.timeout = timeout
		self.formatFile = "default.cfg"

		self.startTests()


	def startTests(self):
		"""
		Loops gathering data from input files and then uses them on a request.
		"""
		while (self.test_files):
			mfs = CustomHTTPLib(self.host, self.port, self.formatFile, \
			 self.timeout)
			mfs.connect()
			plain_data = self.getDictFromJSONFile()
			formated_data = mfs.formatRequest(plain_data)
			mfs.makeRequest(formated_data)
			response = mfs.getResponse()
			self.output(self.currentFilename, response, \
				plain_data['description'], plain_data['status_codes'])


	def getDictFromJSONFile(self):
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
			sys.stderr.write("[ERROR] No JSON object could be decoded - %s\n" \
			 % self.currentFilename)
			if self.test_files:
				return self.getDictFromJSONFile()
			sys.exit(2)

	def output(self, filename, response, description, statusCodes):
		"""
		Prints how the test went.
		"""
		print self.analizeStatusCode(response, statusCodes), \
		 "["+filename+"] |", description

	def analizeStatusCode(self, response, statusCodes):
		"""
		Returns a human readable representation of the result status of the 
		current test.

		"""
		if response.status in statusCodes:
			return "[!!] Missed"
		else:
			return "[+] Blocked"


if __name__ == "__main__":
    sys.stderr.write("# Copyright (c) <2012> <Matías Ariel Ré Medina>\n")
    sys.stderr.write("# pyronbee, idea from ivanr's waf-research\n")

    if len(sys.argv) >= 4:
    	pb = PyronBee(sys.argv[1], int(sys.argv[2]), sys.argv[3:])

    else:
        print "[!] Usage: %s host port test_files" % sys.argv[0]
        print "[!] Examples:"
        print "\t %s mfsec.com.ar 80 request.test" % sys.argv[0]
        print "\t %s mfsec.com.ar 443 *.test" % sys.argv[0]
        sys.exit(2)