#
#	This class provides some functionality for 
#	manipulating status messages when necessary.
#

class TwitterUtils():

	#	This function gives a sterilized version of the status.
	def StatusTextWithoutHashtagsAndMentions(self, status):

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
