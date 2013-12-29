#
#	This class downloads the movies from 
#	Twitter and parses them out for us.
#

from keys import APIKeys
import twitter
import time

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

	status = api.GetRateLimitStatus()
	
	#	Track the rate limiting...
	remaining_requests = int(status["resources"]["search"]["/search/tweets"]["remaining"])
	
	reset_time = int(status["resources"]["search"]["/search/tweets"]["reset"])
	current_time =  time.time()

	time_left = reset_time - current_time
	
	if (remaining_requests == 0):
		print "We're out of requests until " + str(reset_time) + "! (That's in " + str(int(reset_time) - int(current_time)) + " seconds.)"
		return


	#	Search Twitter for the tweets.
	#	
	#	First we need a list to put the tweets into.
	#	We also need a max_id to use as a cursor.

	allRelevantTweets = list()	#	lists are the default collection object in our API.

	max_id = None		#	Used for pagination
	current_search = 1  #	Used for logging	

	#	Now, "prime the pump" by getting the original tweets
	relevantTweets = api.GetSearch("#ifthemoviewerejewish", None, None, max_id, None, 100, None, None, 'mixed', None)

	#	So long as we have more tweets, keep going.
	while (len(relevantTweets) > 0):

		#	Increment/log the current search...
		current_search += 1
		print "Search segment #" + str(current_search)

		#	Put the previous results at the end of our list object
		allRelevantTweets.extend(relevantTweets)

		#	In Python, we can query a list from the end, using negative indices
		max_id = int(relevantTweets[-1].id)

		#	Now go fetch a new set of tweets.
		relevantTweets = api.GetSearch("#ifthemoviewerejewish", None, None, max_id, None, 100, None, None, 'mixed', None)


	#	The next move is to filter retweets and duplicates.
	#	This will make it simpler when we query IMDb.
	allRelevantTweets = filterDupes(allRelevantTweets)

	#	Print out all of the tweets
	for tweet in allRelevantTweets:
		print tweet.user + ": " + tweet.GetText() 



#	This function filters the duplicates out...
def filterDupes(seq): 
   # order preserving
   noDupes = []
   [noDupes.append(i) for i in seq if not noDupes.count(i)]
   return noDupes

#	This function prints the dictionaries and their values:
def printKeyValuePairs(dictionary):
	for key in dictionary:
		print key



# This kicks off the program
main()