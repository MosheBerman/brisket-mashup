import urllib 	#	Sanitizing content
import urllib2	#	Web requests
import ast 		#	Assists with converting strings to dictionaries	
from Movie import Movie

#
#	This class searches IMDb and returns the search results
#

class IMDbSearch():
	
	#	Returns a collection of Movie objects
	def SearchTitle(self, title):

		try:
			#	Make the URL safe for using
			title = title.replace("\n", "")
			title = urllib.quote(title)
		except KeyError, e:
			print "Failed to escape title: " + title

		searchString = "http://www.imdb.com/xml/find?json=1&nr=1&tt=on&q=" + title

		return self.ExecuteSearch(searchString)

	def ExecuteSearch(self, url):

		try:
			pass

			#	Download the results
			search_results = urllib2.urlopen(url).read()

			#	Convert to a dictionary
			results_dictionary = dict()

			try:
				results_dictionary = ast.literal_eval(search_results)
			except SyntaxError, e:
				print "Failed to load movies for URL : " + str(url)
				return None
			except ValueError, e:
				print "Failed to load movies for URL : " + str(url)
				return None
			except Exception, e:
				print "Failed to load movies for URL : " + str(url)
				return None


			#	The metadata
			collection_of_movie_metada = list()

			collection_of_movie_metada.extend(results_dictionary.get("title_exact", dict()))
			collection_of_movie_metada.extend(results_dictionary.get("title_approx",dict()))
			collection_of_movie_metada.extend(results_dictionary.get("title_popular",dict()))

			if len(collection_of_movie_metada) == 0:
				print "Failed to load movies for URL : " + str(url)
				return None

			#	Collect the actual movies
			movies = list()

			#	Iterated the metadata and convert to objects
			for movie_data in collection_of_movie_metada:
				
				movie = Movie(movie_data)

				movies.append(movie)

			return movies

		except Exception, e:
			return None