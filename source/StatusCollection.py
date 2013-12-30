#
#	This class represents a collection of status
#	messages that paroday or reference a movie.
#
#	It contains the movie object as well as 
#	a list of Status objects.
#

class StatusCollection():

	def __init__(self, movie, statuses):
		self.movie = movie
		self.statuses = statuses
