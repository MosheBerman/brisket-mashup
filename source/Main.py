#
#	This is where the magic happens!
#

from TwitterFetcher import TwitterFetcher 
from TwitterUtils import TwitterUtils
from IMDbSearch import IMDbSearch
from StatusCollection import StatusCollection
from HTMLGenerator import HTMLGenerator

import os
import gc
import codecs

def main():

	print "Preparing some ojects to work with..."

	#	This is where our results will live.
	#	We can use this for rendering a display
	finalPairings = list()

	#	An object that fetches status message from Twitter
	twitter = TwitterFetcher()

	#	The IMDb search "engine"
	imdb = IMDbSearch()

	#	The Twitter Utils 
	utils = TwitterUtils()

	#	The HTML Generator 
	html = HTMLGenerator()

	print "Finding twitter statuses that contain #IfTheMovieWereJewish..."

	#	This line fetches filtered tweets in which
	#	the authors parody movie names
	statusesThatParodyMovieNames = twitter.PerformFetch()

	print "Finding the movies that were being parodied by their respective Tweeps..."

	if statusesThatParodyMovieNames == None:
		print "Failed to gather tweets; can't proceed; aborting."
		return


	print "Pairing tweets with movies..."

	gc.disable()

	#	Loop through the tweets and try to 
	#	find the movies that they match.
	for status in statusesThatParodyMovieNames:
		
		status_text = utils.StatusTextWithoutHashtagsAndMentions(status)
		status_text.replace(" ", "+")

		relevant_movies = imdb.SearchTitle(status_text)

		pairing = StatusCollection(relevant_movies, [status])

		finalPairings.append(pairing)

	gc.enable()

	#
	#	Print out the results
	#

	print "Rendering webpage with results..."
	webpage = html.RenderPairings(finalPairings)

	if type(webpage) == unicode:
		webpage.encode("utf_8", 'ignore')


	#
	#	Save them into a webpage
	#
	print "Saving the webpage..."

	path = os.path.join(os.getcwd(), "jewish-movies.html")


	with open(path, "w") as text_file:
		text_file.write(webpage)

	print "Done!"

main()