#
#	This is where the magic happens!
#

from TwitterFetcher import TwitterFetcher 
from TwitterUtils import TwitterUtils
from IMDbSearch import IMDbSearch
from StatusCollection import StatusCollection

def main():

	print "Preparing some ojects to work with..."

	#	This is where our results will live.
	#	We can use this for rendering a display
	finalPairings = dict()

	#	An object that fetches status message from Twitter
	twitter = TwitterFetcher()

	#	The IMDb search "engine"
	imdb = IMDbSearch()

	#	The Twitter Utils 
	utils = TwitterUtils()

	print "Finding twitter statuses that contain #IfTheMovieWereJewish..."

	#	This line fetches filtered tweets in which
	#	the authors parody movie names
	statusesThatParodyMovieNames = twitter.PerformFetch()

	print "Finding the movies that were being parodied by their respective Tweeps..."

	if statusesThatParodyMovieNames == None:
		print "Failed to gather tweets; can't proceed; aborting."
		return

	#	Loop through the tweets and try to 
	#	find the movies that they match.
	for status in statusesThatParodyMovieNames:
		
		status_text = utils.StatusTextWithoutHashtagsAndMentions(status)
		status_text.replace(" ", "+")

		relevant_movies = imdb.SearchTitle(status_text)

		if(relevant_movies != None and len(relevant_movies) > 0):
			best_matching_movie = relevant_movies[0]
			movie_id = best_matching_movie.id

			#	Using the movie ID as a key, if the movie  
			#	was never paired before, use its movie_id
			#	as the key for the pairing.
			if not movie_id in finalPairings:
				 pairing = StatusCollection(best_matching_movie, [status])
				 finalPairings[movie_id] = pairing

			#	Otherise, just key in and add the status
			else:
				finalPairings[movie_id].statuses.append(status)


	print "Printing results..."

	#	Print the results
	for key in finalPairings:

		pairing = finalPairings[key]

		print "-----"
		print "Movie: " + pairing.movie.title 
		print "Tweets: "
		for status in pairing.statuses:
			print "\t" + status.text

main()