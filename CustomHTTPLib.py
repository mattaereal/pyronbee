#!/usr/bin/env python

import socket, sys
from json import load as JSONLoad
from urllib import urlencode
from StringIO import StringIO
from httplib import HTTPResponse

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

		data = self.sock.recv(1024)
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
		
		for header, value in data["headers"].iteritems():
			request += self.format['header'] % (header, value)

		request += self.format['body'] % urlencode(data['body'])

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
