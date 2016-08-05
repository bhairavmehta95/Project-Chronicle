 # -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import re
from wiki import search_and_process

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
		try:
			title = title.replace("–", "-")
			url_list.append(url)
			title_list.append(title)
		except:
			pass

title_list.sort()
url_list.sort()

# testing
search_and_process(title_list[5])