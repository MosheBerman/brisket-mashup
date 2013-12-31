#
#	This class downloads the movies from 
#	Twitter and parses them out for us.
#

from keys import APIKeys					#	Abstract out aPI keys for privacy
from TwitterUtils import TwitterUtils		#	Utility to manipulate Tweets
import twitter 	#	Basis for twitter operations
import time 	#	Used for counting time until rate limit ends
import gc

class TwitterFetcher():

	def PerformFetch(self):

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

		gc.disable()

		#	So long as we have more tweets, keep going.
		while (len(relevant_tweets) > 0):

			#	Increment/log the current search...
			current_search += 1

			#	Put the previous results at the end of our list object
			all_relevant_tweets.extend(relevant_tweets)

			#	In Python, we can query a list from the end, using negative indices
			max_id = int(relevant_tweets[-1].id)

			#	Now go fetch a new set of tweets.
			relevant_tweets = api.GetSearch(search_term, None, None, max_id, None, 100, None, None, 'mixed', None)

			#	If we reloaded the last Tweet and have nothing new, let's terminate the loop.
			if len(relevant_tweets) == 1 and relevant_tweets[-1].id == max_id:
				relevant_tweets = list()

		gc.enable()

		print "Fetched " + str(len(all_relevant_tweets)) + " tweets containing the hashtag #ifthemoviewerejewish. Filtering... "

		#	The next move is to filter retweets and duplicates.
		#	This will make it simpler when we query IMDb.
		#all_relevant_tweets = self.FilterDupes(all_relevant_tweets)

		#	Now we remove any tweets with URLs in them. Odds are
		#	we don't want them.
		#all_relevant_tweets = self.FilterTweetsContainingURLS(all_relevant_tweets)

		#	Remove hashtags and users from tweets, then count words.
		#	Statuses that are longer than our max length after discarding
		#	hashtag and mention metadata are filtered out.
		#all_relevant_tweets = self.TweetsShorterThanMaximumLength(all_relevant_tweets, desired_max_length)

		all_relevant_tweets = self.EfficientlyFilteredTweets(all_relevant_tweets, desired_max_length)

		print "After filtering, " + str(len(all_relevant_tweets)) + " remain."

		#	Finally return all the relevant tweets
		return all_relevant_tweets

	#	This function combines the filters in the three methods that follow it into a single loop for performance
	def EfficientlyFilteredTweets(self, original_list, max_length):
		#	This is the list we return with retweets filtered out.
	  	unique_list = list()

	  	#	The texts that we want.
	  	list_of_status_texts_seen = list()


	  	manipulator = TwitterUtils()

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

	  		#	Filter URLS
	  		if len(status.urls) > 0:
				continue

			if "http://" in status.text:
				continue

			#	Remove hashtags and then count the length	
			status_text = manipulator.StatusTextWithoutHashtagsAndMentions(status)

			#	If the movie name is less than or equal to
			#	our length, then include it.
			if(len(status_text.split()) > max_length):	
				continue

	  		#	Otherwise, we have a decent chance of a clean status.
	  		unique_list.append(status)

	  	#	Don't forget to return!
	  	return unique_list

	#	This function filters the duplicates out...
	def FilterDupes(self, original_list): 

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

	  	#	Don't forget to return!
	  	return unique_list



	#	This function filters out tweets containing URLs
	def FilterTweetsContainingURLS(self, original_list):

		#	The list of filtered URLs
		linkless_statuses = list()

		for status in original_list:
			if len(status.urls) == 0:
				linkless_statuses.append(status)

		return linkless_statuses


	#	Filters out all tweets that are longer than 
	#	The defined length, not including hashtags
	def TweetsShorterThanMaximumLength(self, original_list, length):

		short_list = list()

		manipulator = TwitterUtils()

		for status in original_list:
			#	Remove hashtags and then count the length	
			status_text = manipulator.StatusTextWithoutHashtagsAndMentions(status)

			#	If the movie name is less than or equal to
			#	our length, then include it.
			if(len(status_text.split()) <= length):	
				short_list.append(status)

		return short_list

	
	#	This function print out the texts of statues messages
	#	in a supplied list and also prints the length of the list.
	def PrintList(self, list):

		print "\n\n------------\nPrinting list of " + str(len(list)) + " statuses.\n------------\n\n"

		for status in list:
			print "------------\n" + status.text + "\n------------\n"

