#
#	This contains keys for our Twitter API Requests
#

#
#	Twitter API Keys - encapsulated as an object for importing.
#

class APIKeys():

	def __init__(self):
		self.kConsumerKey = ""
		self.kConsumerSecret = ""
		self.kAccessToken = ""
		self.kAccessTokenSecret = ""

	def getConsumerKey(self):
		return self.kConsumerKey

	def getConsumerSecret(self):
		return self.kConsumerSecret

	def getAccessToken(self):
		return self.kAccessToken

	def getAccessTokenSecret(self):
		return self.kAccessTokenSecret		


