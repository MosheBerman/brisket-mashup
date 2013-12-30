#
#	This class provides some functionality for 
#	manipulating status messages when necessary.
#

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

		return status_text