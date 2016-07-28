from speech import speech_query
from nltk.corpus import stopwords
import urllib
import urllib2
from bs4 import BeautifulSoup
import wikipedia

def wiki_search(subject):

	## KEEP TO POTENTIALLY SEARCH OTHER SOURCES ##

	# subject = urllib.quote(subject)
	# subject.replace (" ", "_")

	# opener = urllib2.build_opener()
	# opener.addheaders = [('User-agent', 'Mozilla/5.0')] #wikipedia needs this

	# url = "http://en.wikipedia.org/wiki/" + subject
	# data = urllib.urlopen(url)
	# soup = BeautifulSoup(data, "html.parser")

	#text =  soup.find('div',id="bodyContent")
	# text = soup.get_text().encode('utf-8')

	# gets a list of common stop words
	stopWords = set(stopwords.words('english'))

	# gets wikipedia page based on subject
	text = wikipedia.page(subject).content.encode('utf-8')

	# checking 
	
	# formats text
	text = text.lower()
	text = text.rstrip()
	text = text.translate(None, '!@#$%^*():;,./-_[]}{+=~')
	
	# removes stop words
	text = ' '.join([word for word in text.split() if word not in stopWords])

	text_dictionary = {}
	word_count = 0

	# creates a hash table with [word] : occurance

	for word in text.split():
		if text_dictionary.get(word) == None :
			text_dictionary[word] = 1
		else:
			text_dictionary[word] = text_dictionary[word] + 1

		# tracks total word count
		word_count += 1

	### FOR TESTING
	file = open("newfile.txt", "w")

	for word in text_dictionary:
		string = str(word) + ' : ' + str(text_dictionary[word]) + '\n'
		file.write(string)

	###

	print "Response time!"
	# gets response from microphone
	reponse = speech_query()


	# formats reponse
	reponse = reponse.lower()
	
	# removes stop words
	reponse = ' '.join([word for word in reponse.split() if word not in stopWords])

	# calculates score, and outputs it

	score = 0

	response_dictionary = {}
	print "RESPONSE:", reponse

	for word in reponse.split():
		if text_dictionary.get(word) != None and response_dictionary.get(word) == None:
			score += text_dictionary[word]

			# arbitrary value to show the word has been marked
			response_dictionary[word] = True
		else:
			pass


	percentage = score / float(word_count) * 100
	print "You scored a:", percentage, " percent out of 100%"

def search_and_process():
	subject = speech_query()
	wiki_search(subject)


if __name__ == "__main__":
	search_and_process()