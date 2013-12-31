#
#	This class provides some functionality for 
#	manipulating status messages when necessary.
#

import re

class TwitterUtils():

	#	This function gives a sterilized version of the status.
	def StatusTextWithoutHashtagsAndMentions(self, status):

		status_text = status.text.lower()

		#	Remove hashtags
		for hashtag in status.hashtags:
			status_text = status_text.replace(hashtag.text.lower(), "")

		#	Remove hashtag marks
		status_text = status_text.replace("#", "")

		#	Remove mention symbols
		status_text =  status_text.replace("@", "")

		#	Remove screen names
		for mention in status.user_mentions:
			status_text = status_text.replace(mention.screen_name.lower(), "")

		# #	If there's a quote, we want to unwrap its contents
		# status_text = status_text.replace(u"\u2018", "'").replace(u"\u2019", "'").replace(u"\u201c", "'").replace(u"\u201d", "'")

		# if status_text.count('"') == 2:
		# 	status_text = status_text.split('"')[1].split('"')[0]

		# if status_text.count("'") == 2:
		# 	status_text = status_text.split("'")[1].split("'")[0]

		#	While we're at it, remove all non-alphanumerics
		status_text = re.sub('[^0-9a-zA-Z] +', '', status_text)

		return status_text