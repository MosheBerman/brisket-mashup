#
#	This class generates HTML based on a StatusPairing object
#

class HTMLGenerator():
	
	#	Renders a list of pairings
	def RenderPairings(self, pairings):

		HTML  = '<!DOCTYPE html>\n<html>\n<head>\n<title>#IfTheMovieWereJewish\n</title>\n<link rel="stylesheet" type="text/css"  href="./style.css" />\n'
		HTML += '\n\t<script type="text/javascript" src="./date-formatter.js">'
		HTML += '\n\t</script>'
		HTML += '\n\t<script type="text/javascript">'
		HTML += '\n\t\twindow.onload = function(){ console.log("Formatting dates"); formatDates(); };'
		HTML += '\n\t</script>'
		HTML +='\n</head>\n<body>'

		for pair in pairings:
			HTML += self.RenderPair(pair)

		HTML += '</body>\n</html>'

		return HTML

	#	Generates an HTML rendering of a 
	#	pairing between movies and a tweet.
	def RenderPair(self, pairing):

		#	Unwrap the statuses and movies (assume one status)
		status = pairing.statuses[0]	
		movies = pairing.movies

		#	Prepare the HTML
		HTML = '\n\t<div class="pairing">'
		HTML += self.RenderStatus(status)
		

		if (movies == None) or (len(movies) == 0):
			HTML += '\n\t\t<div class="no-movies">\n\t\t\t\tNo movies'
		else:

			HTML += '\n\t\t<div class="movies">'
			HTML += '\n\t\t\t<div class="movies-wrapper">'
			
			for movie in movies:
				HTML += self.RenderMovie(movie)
				if len(movies) > 1 and movie.id != movies[-1].id:
				 	HTML += ", "

			HTML += '\n\t\t\t</div>'

		HTML += '\n\t\t</div>'
		HTML += '\n\t</div>'

		return HTML


	#	This method renders HTML from a status message
	def RenderStatus(self, status):
		
		#	Render the tweet content
		processed_content = self.RenderTweetContent(status)

		#	Render the content
		HTML = '\n\t\t<div class="tweet">'
		HTML += '\n\t\t\t<div class="tweet-real-name">'
		HTML += '\n\t\t\t\t<h2>' + status.user.name + '</h2>'
		HTML += '\n\t\t\t</div>'
		HTML += '\n\t\t\t<div class="tweet-user-name">'
		HTML += '\n\t\t\t\t<h3>\n\t\t\t\t\t' + self.RenderLinkToUser(status.user.screen_name, True) 
		HTML += '\n\t\t\t\t</h3>'
		HTML += '\n\t\t\t</div>'		
		HTML += '\n\t\t\t<div class="tweet-content">'
		HTML += '\n\t\t\t\t' + processed_content
		HTML += '\n\t\t\t</div>'		
		HTML += '\n\t\t\t<div class="tweet-timestamp">'
		HTML += '\n\t\t\t\t' + str(status.created_at_in_seconds)
		HTML += '\n\t\t\t</div>'
		HTML += '\n\t\t</div>'
		
		return HTML

	#	This method renders HTML from a movie
	def RenderMovie(self, movie):

		#	Render the content
		HTML =  '\n\t\t<div class="movie">'
		HTML += '\n\t\t\t\t<a href="http://imdb.com/title/' + movie.id + '" class="movie-title"><span id="'+movie.id+'"></span>' + movie.title + '</a>'
		HTML += '\n\t\t</div>'

		return HTML

	#	This method converts mentions and hashtags into links.
	def RenderTweetContent(self, tweet):
		
		#	Pull out the text of the tweet while removing hash and @ symbols. 
		content = tweet.text.replace("#", "").replace("@", "")

		#	Render links in place of the hashtag
		for hashtag in tweet.hashtags:
			content = content.replace(hashtag.text, self.RenderHashtagLink(hashtag.text))

		for mention in tweet.user_mentions:
			screen_name = mention.screen_name
			content = content.replace(screen_name, self.RenderLinkToUser(screen_name, True))

		return content 


	#	Renders a hashtag search link
	#	https://twitter.com/search?q=%23ifthemoviewerejewish&src=hash
	def RenderHashtagLink(self, hashtag_text):
		return '<a href="https://twitter.com/search?q=%23' + hashtag_text + '&src=hash" class="hashtag-link">#' + hashtag_text + "</a>" 

	#	Renders a link to a user profile on twitter.
	def RenderLinkToUser(self, user_name, is_mention):
		if is_mention != True:
			is_mention = False

		return '<a href="http://twitter.com/' + user_name + '" class="user-link">' + ("@" if is_mention else "") + user_name + "</a>"
