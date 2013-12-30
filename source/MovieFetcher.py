#
#	This class downloads the movies from 
#	Twitter and parses them out for us.
#

from APIKeys import APIKeys
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

	all_relevant_tweets = list()	#	lists are the default collection object in our API.

	max_id = None											#	Used for pagination
	current_search = 1 						 				#	Used for logging	
	search_term = "#ifthemoviewerejewish"					#	The hashtag to search for
	desired_max_length = 6									#	The maximum number of words after removing hashtags

	#	Now, "prime the pump" by getting the original tweets
	relevant_tweets = api.GetSearch(search_term, None, None, max_id, None, 100, None, None, 'mixed', None)

	#	So long as we have more tweets, keep going.
	while (len(relevant_tweets) > 0):

		#	Increment/log the current search...
		current_search += 1
		print "Loading the next segment of status results #" + str(current_search)

		#	Put the previous results at the end of our list object
		all_relevant_tweets.extend(relevant_tweets)

		#	In Python, we can query a list from the end, using negative indices
		max_id = int(relevant_tweets[-1].id)

		#	Now go fetch a new set of tweets.
		relevant_tweets = api.GetSearch(search_term, None, None, max_id, None, 100, None, None, 'mixed', None)

		#	If we reloaded the last Tweet and have nothing new, let's terminate the loop.
		if len(relevant_tweets) == 1 and relevant_tweets[-1].id == max_id:
			relevant_tweets = list()

	#	The next move is to filter retweets and duplicates.
	#	This will make it simpler when we query IMDb.
	all_relevant_tweets = FilterDupes(all_relevant_tweets)

	#	Now we remove any tweets with URLs in them. Odds are
	#	we don't want them.
	all_relevant_tweets = FilterTweetsContainingURLS(all_relevant_tweets)

	#	Remove hashtags from tweets 
	all_relevant_tweets = TweetsShorterThanMaximumLength(all_relevant_tweets, desired_max_length)



#	This function filters the duplicates out...
def FilterDupes(original_list): 

	#	This is the list we return with retweets filtered out.
  	unique_list = list()

  	#	The texts that we want.
  	list_of_status_texts_seen = list()

  	#	For each status message, let's check the text agains seen texts.
  	#	If we've seen it, or it contains "RT", "via", "retweet", throw it away.
  	#	Otherwise, add the text to the seen texts list and keep the status.

  	for status in original_list:
  		status_text = status.text
  		
  		 #	Bypass retweets
  		if "RT" in status_text or "retweet" in status_text or "via" in status_text:
  			continue

  		#	Bypass duplicates that were independently thought of
  		if status_text in list_of_status_texts_seen:
  			#	TODO: Find a way to attach the second tweeter to the original status?
  			continue

  		#	Otherwise, we have a decent chance of a single tweet.
  		unique_list.append(status)

  	#	Don't forget to return!
  	return unique_list


#	This function filters out tweets containing URLs
def FilterTweetsContainingURLS(original_list):

	#	The list of filtered URLs
	linkless_statuses = list()

	for status in original_list:
		if len(status.urls) == 0:
			linkless_statuses.append(status)

	return linkless_statuses


#	Filters out all tweets that are longer than 
#	The defined length, not including hashtags
def TweetsShorterThanMaximumLength(original_list, length):

	short_list = list()

	for status in original_list:
		#	Remove hashtags and then count the length	
		status_text = StatusTextWithoutHashtagsAndMentions(status)

		#	If the movie name is less than or equal to
		#	our length, then include it.
		if(len(status_text.split()) <= length):	
			short_list.append(status)

	return short_list

#	This function gives a sterilized version of the status.
def StatusTextWithoutHashtagsAndMentions(status):

	status_text = status.text

	#	Remove hashtag marks
	status_text.replace("#", "")

	#	Remove hashtags
	for hashtag in status.hashtags:
		status_text.replace(hashtag.text, "")

	#	Remove mention symbols
	status_text.replace("@", "")

	#	Remove screen names
	for mention in status.user_mentions:
		status_text.replace(mention.screen_name, "")

	return status_text

#	This function print out the texts of statues messages
#	in a supplied list and also prints the length of the list.
def PrintList(list):

	print "\n\n------------\nPrinting list of " + str(len(list)) + " statuses.\n------------\n\n"

	for status in list:
		print "------------\n" + status.text + "\n------------\n"

# This kicks off the program
main()