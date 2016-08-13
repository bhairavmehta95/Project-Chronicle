 # -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting, Student, Enrollments, Class, Topic, Question, Testing

from .forms import SignupForm

from wiki import wiki_search

from bs4 import BeautifulSoup
import requests
import re
from wiki import search_and_process
import json


# Create your views here.
def index(request):
    if request.method == 'POST':
        form = SignupForm()
        return render(request, 'signup.html', {'form': form})

    return render(request, 'index.html')

def speech(request, class_id, topic_id, question_id):
    q = Question.objects.get(class_id = class_id, topic_id = topic_id, question_id = question_id)

    if request.method == 'POST':
        print request.POST.get('transcript', "Didn't find")

    return render(request, 'speech.html', {'q' : q})
def signup_user(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SignupForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            f_name_new = form.cleaned_data['f_name']
            l_name_new = form.cleaned_data['l_name']

            # TO DO: Check the user information before adding
            # TO DO: Autoincrement student_id
            # TO DO: Add email and password?

            s = Student(student_id = 1, f_name = f_name_new, l_name = l_name_new)
            s.save()

            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            print "Thanks!"
            return render(request, 'index.html')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})

def class_page(request):
    classes = Class.objects.all()

    return render(request, 'class.html', {'classes': classes})

def topic_page(request, class_id):
    topics = Topic.objects.all().filter(class_id = class_id)

    # TO DO: How to configure the URL the right way, currently passes in correct topics
    return render(request, 'topics.html', {'topics' : topics})
    

def question_page(request, class_id, topic_id):
    questions = Question.objects.filter(class_id = class_id).filter(topic_id = topic_id)

    # TO DO: How to configure the URL the right way, currently passes in correct topics
    return render(request, 'questions.html', {'questions' : questions})

def db(request):

    ## TESTING AREA FOR FUNCTIONS 
    q = Question.objects.all()

    for qu in q:
        try:
            print qu.topic_id, " within ", qu.class_id
        except:
            print "ascii err"

    return render(request, 'db.html', {'t': q})

    ### TESTING AREA END

    # Resets DB (testing only)
    Class.objects.all().delete()
    Question.objects.all().delete()
    Topic.objects.all().delete()

    # creates history class, gets that object
    class_ = Class.objects.create(class_name = "History")
    
    
    print class_

    # Scrapes for US History page on wikipedia
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

    total_count = 1

    for topic in title_list:
        question_dict = search_and_process(topic)

        i = 0
        while i < len(question_dict['topics']):
            print topic
            question = question_dict['topics'][i]
            question_text = question_dict['text'][i]
            i += 1

            # Creating the topics, and the questions
            # TO DO: Make separate

            # tries to find the topic, otherwise adds it
            try:
                topic_add = Topic.objects.get(topic_name = topic)
            except:
                topic_add = Topic.objects.create(class_id = class_, topic_name = topic)

            # adds, saves question
            question_add = Question.objects.create(
                class_id = class_,
                topic_id = topic_add,
                question_subject = question,
                question_text = question_text,
                )



#
    # greeting = Greeting()
    # greeting.save()

    # greetings = Greeting.objects.all()

    # s = Student(student_id = 1, f_name = "bhairav", l_name = "mehta")

    # s.save()

    q = Question.objects.all()

    return render(request, 'db.html', {'t': q})

