#from nltk.corpus import stopwords
import urllib
import urllib2
#from bs4 import BeautifulSoup
import wikipedia

import speech_recognition as sr
from threading import Thread, Event

exitFlag = 0

# TODO: 
# Add questions to DB
# Create Hash tables for each one
# Add Link "clicking" -- web scraping

# function that uses Google Speehc Recongition to understand micrphone
def speech_query():
    r = sr.Recognizer()
    m = sr.Microphone()

    try:
        print("A moment of silence, please...")
        with m as source: r.adjust_for_ambient_noise(source)
        print("Set minimum energy threshold to {}".format(r.energy_threshold))

        print("Say something!")
        with m as source: audio = r.listen(source)
        print("Got it! Now to recognize it...")
        try:
            # recognize speech using Google Speech Recognition
            value = r.recognize_google(audio)

            # we need some special handling here to correctly print unicode characters to standard output
            if str is bytes: # this version of Python uses bytes for strings (Python 2)
                print(u"You said {}".format(value).encode("utf-8"))
            else: # this version of Python uses unicode for strings (Python 3+)
                print("You said {}".format(value))

            return value
        except sr.UnknownValueError:
            print("Oops! Didn't catch that")
        except sr.RequestError as e:
            print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
    except KeyboardInterrupt:
        pass

# searches a wikipedia subject
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
	#stopWords = set(stopwords.words('english'))

	### UNCOMMENT WHEN WITH INTERNET ###
	
	# gets wikipedia page based on subject
	text = wikipedia.page(subject).content.encode('utf-8')

	# Writes all text to text file, and then reads it (TODO: do this better somehow)

	w = open('text.txt', 'w')
	w.write(text)

	### END COMMENT BLOCK ###

	r = open('text.txt', 'r')
	text = r.read()
	text = str(text)

	# creates question dictionary, each has a list
	question_dict = {'topics': [], 'text': []}

   	# main = text.split('=')[0]
   	# text = text.split('=')[1]
   	main = ''
   	#lines = iter(lines)

   	# Developing the questions
   	for line in text.split('\n'):
   		if line == '\n' or line == None or line == ' ' or line == '':
   			continue

   		if line[0] != '=':
   			main += str(line)

   		elif line[0] == '=':
   			if main != '':
	   			question_dict['topics'].append(subject)
	   			question_dict['text'].append(main)

			subject = str(line)
			main = ''

	# gets last one
	if main != '':
		question_dict['topics'].append(subject)
	   	question_dict['text'].append(main)

	# formats topic and text, removes symbols, newlines, and stopwords
	i = 0
	while i < len(question_dict['topics']):
		question_dict['topics'][i] = question_dict['topics'][i].translate(None, '\n!@#$%^*:;,./_[]}{+=~"')
		i += 1

	i = 0
	while i < len(question_dict['text']):
		question_dict['text'][i] = question_dict['text'][i].lower()
		question_dict['text'][i] = question_dict['text'][i].rstrip()
		question_dict['text'][i] = question_dict['text'][i].translate(None, '\n!@#$%^*():;,./-_[]}{+=~"')
	
		# removes stop words
		#question_dict['text'][i] = ' '.join([word for word in question_dict['text'][i].split() if word not in stopWords])
		i += 1

	# print 'topic', len(question_dict['topics']), question_dict['topics'][2]
	# print 'question', len(question_dict['text']), question_dict['text'][2]

	return question_dict


	# Function that opens a file and reads a user response,
	# Put function (parts of it) into views.py
	def user_response():
		w = open('text.txt', 'w')

		i = 0
		while i < len(question_dict['text']):
			w.write(question_dict['topics'][i])
			w.write(question_dict['text'][i])
			w.write('\n')


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
		#reponse = ' '.join([word for word in reponse.split() if word not in stopWords])

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

def search_and_process(subject):
	#subject = speech_query()
	question_dict = wiki_search(subject)
	
	return question_dict


if __name__ == "__main__":
	search_and_process("History of the world")