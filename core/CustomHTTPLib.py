#!/usr/bin/env python
# -*- coding: latin-1 -*-

# Copyright (c) <2012> Matías Ariel Ré Medina <mre@infobytesec.com> 

# Custom HTTP lib using sockets module part from pyronbee as a module.

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


import socket, sys
from json import load as JSONLoad
from urllib import urlencode
from StringIO import StringIO
from httplib import HTTPResponse
from base64 import decodestring as decode

class CustomHTTPLib:
	"""
	Custom HTTP lib using nothing but sockets.
	"""

	def __init__(self, host, port, formatFile="default.cfg", timeout=10):
		self.host = host
		self.port = port
		self.timeout = timeout # for future implementations.
		self.sock = None
		self.format = {}
		self.formatFile = formatFile

		self.getConfig()

	def getConfig(self):
		"""
		Gathers current configuration file for formats.
		"""

		self.format = self.getDictFromJSONFile(self.formatFile)

	
	def connect(self):
		"""
		Opens a plain tcp connection to self.host:self.port.
		"""
		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error, msg:
			sys.stderr.write("[ERROR] %s\n" % msg[1])
			sys.exit(1)

		try:
			self.sock.connect((self.host, self.port))
		except socket.error, msg:
			sys.stderr.write("[ERROR] %s\n" % msg[1])
			sys.exit(2)

		return self.sock

	def makeRequest(self, data):
		"""
		Sends data through the opened socket.
		"""
		self.sock.send(data)
		data = self.sock.recv(1024) ##problema
		self.plain_response = ""
		while len(data):
			self.plain_response = self.plain_response + data
			data = self.sock.recv(1024)
		self.sock.close()

	def getResponse(self):
		"""
		Returns an HTTP response object.
		"""
		self.__httpparse__()
		return self.response
	
	def __httpparse__(self):

		socket = FakeSocket(self.plain_response)
		self.response = HTTPResponse(socket)
		self.response.begin()

	def getDictFromJSONFile(self, currentFilename):
		"""
		Reads the request data stored in the file with JSON syntax.
		"""
		try:
			currentFile = open(currentFilename)
			data = JSONLoad(currentFile)
			currentFile.close()
			return data
		except:
			sys.stderr.write("[ERROR] No JSON object could be decoded - %s" \
			 % currentFilename)
			sys.exit(2)

	def formatRequest(self, data):
		"""
		Formatting the raw data into a valid HTTP request.
		"""
		request = self.format['method'] % (data['method'], data['url'], \
		 data['http_ver'])
		
		request += self.format['header'] % ("Host", self.host)
		for header, value in data["headers"].iteritems():
			request += self.format['header'] % (header, value)


		"""
		When a POST method is used, here you control the data. Actually, since \
		this tool intends to be liberal, you may use both when testing wafs, \
		so feel free to take out the next if else sentence if you want to.
		"""
		
		if data['urlencoded']:
			request += self.format['data'] % urlencode(data['urlencoded'])
		elif data['multipart']:
			request += self.format['data'] % decode(data["multipart"])
		request += self.format['ending']

		return request

class FakeSocket(StringIO):
	"""
	Just an auxiliary class to trick HTTPResponse.
	"""
	def makefile(self, *args, **kw):
		return self


if __name__ == "__main__":
	mfs = CustomHTTPLib('127.0.0.1', 1337)
	mfs.connect()
	plain_data = mfs.getDictFromJSONFile('request.test')
	formated_data = mfs.formatRequest(plain_data)
	mfs.makeRequest(formated_data)
	response = mfs.getResponse()

	print response.status
