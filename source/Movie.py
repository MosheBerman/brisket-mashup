#
#	This class represents a Movie result from IMDb
#

class Movie():

	def __init__(self, dictionary):
		self.id = dictionary["id"]
		self.title = dictionary["title"]
		self.name = dictionary["name"]
		self.title_description = dictionary["title_description"]
		self.episode_title = dictionary["episode_title"]
		self.description = dictionary["description"]