 # -*- coding: utf-8 -*-

# function that generates the TOPICS based on USHISTORY
#TODO: Make templated/generalized for other classes

from bs4 import BeautifulSoup
import requests
import re
from wiki import search_and_process

print "Hello World!"

result = requests.get('https://en.wikipedia.org/wiki/History_of_the_United_States')

text = result.content
soup = BeautifulSoup(text, 'html.parser')

pattern = re.compile("/wiki/History_of_the_United_States_.")
samples = soup.find_all("a", {'href': pattern})

url_list = []
title_list = []

for item in samples:
	url = item.get('href')
	title = item.get('title').encode('utf-8')

	if url.find('%') != -1 and url.find('#') == -1:
		# ASCII
		title = title.replace("–", "-")
		url_list.append(url)
		title_list.append(title)


title_list.sort()
url_list.sort()

## generates every question, puts them into an output file

file = open('output.txt', 'w')
total_count = 0
for topic in title_list:
	file.write('------ Start of')
	file.write(topic)
	file.write('----------\n\n\n')
	question_dict = search_and_process(topic)
	i = 0
	while i < len(question_dict['topics']):
		print "Question:", question_dict['topics'][i], "inside of ", topic
		file.write(question_dict['topics'][i])
		file.write('\n')
		file.write(question_dict['text'][i])
		file.write('\n')
		i += 1
		total_count += 1
		
	file.write('------ End of')
	file.write(topic)
	file.write('----------\n\n\n')

print total_count