#!/usr/bin/python

import json
import sys
import os
import httplib
import os.path

class Sinusbot:
	jwt_token = '' 		#Auth Token
	botId = ''			#Bot ID required for the Login
	url = ''			#Base URL 
	port = 8087 		#default Sinusbot Port
	ssl = False #		Disable SSL by default
	username = ''
	password = ''
	success_count = 0
	error_count = 0
	extensions=['mp3', 'mp4', 'wav', '3gp']
	
	def __init__(self, url, port, username, password, ssl):
		self.url = url
		self.port = port
		self.ssl = ssl
		self.username = username
		self.password = password
		self.botId = self.DefaultId()
		self.success_count = 0
		self.error_count = 0
		
			
	def DefaultId(self):		
		
		if self.ssl: 
			conn = httplib.HTTPSConnection(self.url, self.port)
		
		else:
			conn = httplib.HTTPConnection(self.url, self.port)
			
		conn.request("GET", "/api/v1/botId")
		response = conn.getresponse()
		
		if response.status == 200:
			j = json.loads(response.read())
			conn.close()
			return j['defaultBotId']
			
				
		else:
			conn.close()
			return ''
		


	def Auth(self):
	
		if self.ssl: 
			conn = httplib.HTTPSConnection(self.url, self.port)
		
		else:
			conn = httplib.HTTPConnection(self.url, self.port)
			
		data =  {"username":self.username, "password":self.password, "botId": str(self.botId)}  #Parse the botId with str() to pre event a golang error in case of unicode
		hdr = {"Content-type": "application/json"}
		
		conn.request("POST", "/api/v1/bot/login", json.dumps(data), hdr)
		response = conn.getresponse()
		
		if response.status == 200:
			response = str(response.read())
			j = json.loads(response)
			
			try:
					self.jwt_token = j['token']
					conn.close()
					self.username = ''
					self.password = '' 
					return True
					
				
			except:	
					conn.close()
					print 'Could not get token: %s' % (response)
					return False
			
		
		else:
			conn.close()
			return False
			
	def Upload(self, LocalPath):
	
		if not os.path.isfile(LocalPath):
			return False
		
			
		try:
			f = open(LocalPath, 'r')
			bytes = f.read()
			f.close()
		except: 
			print 'Could not read -> ' + LocalPath
			return False
		
		if self.ssl: 
			conn = httplib.HTTPSConnection(self.url, self.port)
		
		else:
			conn = httplib.HTTPConnection(self.url, self.port)
			
		hdr = {"Content-type": "application/json", "Authorization": "bearer " + str(self.jwt_token), "Content-Length": len(bytes)}

		conn.request("POST", "/api/v1/bot/upload", bytes, hdr)
		response = conn.getresponse()
		
		
		if response.status == 200:
			conn.close()
			self.success_count += 1
			return True
		else:
			conn.close()
			self.error_count += 1
			return False
		

def uploadHelper(directory, bot, recurse):
	truePath = os.path.abspath(directory)
	contents = os.listdir(truePath)

	for entry in contents:
		entryTruePath = os.path.join(truePath, entry)
		if os.path.isfile(entryTruePath):
			fileExtension = entryTruePath.split('.')[-1]
			if (fileExtension in bot.extensions):
				if bot.Upload(entryTruePath):
					print 'Success uploaded: ' + entryTruePath
				else:
					print 'Error while uploading: ' + entryTruePath
			else:
				print 'File type not supported: ' + entryTruePath
		elif os.path.isdir(entryTruePath) and recurse:
			uploadHelper(entryTruePath, bot, recurse)
		
		
if len(sys.argv) < 6:
	print 'Usage: ./sinusbot_uploader.py 123.124.125.1 port username password LOCAL_DIRECTORY SSL(optional) -R (Recursive)'
	sys.exit(1)
else:
	recursive = False
	if len(sys.argv) >= 7:
		if sys.argv[6] == 'SSL':
			bot = Sinusbot(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], True)
		if sys.argv[6] == '-R' or sys.argv[7] == '-R':
			recursive = True
	else:
			bot = Sinusbot(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], False)
			
			
	if not os.path.isdir(sys.argv[5]):
		print 'LOCAL_DIRECTORY must be a valid directory!'
		sys.exit(1)
		
	bot = Sinusbot(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], False)
	if bot.Auth():
		print 'Success Authenticated!'
		
		dir = os.path.abspath(sys.argv[5])
		files = os.listdir(dir)

		uploadHelper(dir, bot, recurse)					
										
		print 'Completed -> Uploaded %d files with %d errors.' % (bot.success_count, bot.error_count)
										
	else:
		print 'Error on Authentication!'
		sys.exit(1)
