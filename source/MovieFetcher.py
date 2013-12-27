#
#	This class downloads the movies from 
#	Twitter and parses them out for us.
#

from APIKeys import APIKeys
import twitter

def main():

	#	Create a keys object
	keys = APIKeys()

	# Assign the keys to local variables
	consumerKey = keys.getConsumerKey()
	consumerSecret = keys.getConsumerSecret()
	accessToken = keys.getAccessToken()
	accessTokenSecret = keys.getAccessTokenSecret()

	#	Create the Twitter API object
	api = twitter.Api(consumerKey, consumerSecret, accessToken, accessTokenSecret)

	#	Verify credentials and print them out
	#print api.VerifyCredentials()

	#	Search Twitter for all the tweets
	relevantTweets = api.GetSearch("#ifthemoviewerejewish", None, None, None, None, 100, None, None, 'mixed', None)

	for tweet in relevantTweets:
		print tweet.GetText()




# This kicks off the program
main()