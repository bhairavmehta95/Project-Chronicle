 # -*- coding: utf-8 -*-
#
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import Student, Enrollments, Class, Topic, Question, Testing, Completion

from .forms import LoginForm, SignupForm

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from wiki import wiki_search
from bs4 import BeautifulSoup
import requests
import re
from wiki import search_and_process
import json

import random

# Create your views here.
def login_user(request):
    # if this is a POST request we need to process the form data
    error = None
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            # TO DO: Check the user information before adding
            # TO DO: Autoincrement student_id
            # TO DO: Add email and password?
            if user is not None:
                if user.is_active:
                    login(request, user)
                    s = Student.objects.get(user_id_login = user.id)
                    print "Welcome back: ", s
                    # Redirect to a success page.
                    return HttpResponseRedirect('/classes')
                else:
                    error = "Disabled account, contact sysadmin"
                    # Return a 'disabled account' error message
            else:
                error = "Not a valid username or password, please try again."

            return render(request, 'login.html', { 'error' : error, 'form': form})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def signup_user(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SignupForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']
            retyped = form.cleaned_data['retyped']

            # TODO: Assert that password and retyped are the same

            class_id = request.POST['Class']
         
            class_target = Class.objects.get(class_id = class_id)

            # ONLY FOR TESTING
            Student.objects.all().delete()
            User.objects.all().delete()
            Enrollments.objects.all().delete()

            user = User.objects.create_user(username=username,
                                email = email,
                                password=password)

            s = Student.objects.create(user_id_login = user.id, f_name = first_name, l_name = last_name)

            Enrollments.objects.create(student_id = s, class_id = class_target)


            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            print "Welcome", s, "please login"
            return HttpResponseRedirect('/login')
            

    # if a GET (or any other method) we'll create a blank form
    else:
        classes = Class.objects.all()
        form = SignupForm()

    return render(request, 'signup.html', {'form': form, 'classes' : classes})

def class_page(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

    classes = Class.objects.all()
    return render(request, 'class.html', {'classes': classes})

def topic_page(request, class_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

    topics = Topic.objects.all().filter(class_id = class_id)

    return render(request, 'topics.html', {'topics' : topics})

    

def question_page(request, class_id, topic_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

    questions = Question.objects.filter(class_id = class_id).filter(topic_id = topic_id)

    return render(request, 'questions.html', {'questions' : questions})


def speech(request, class_id, topic_id, question_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

    q = Question.objects.get(class_id = class_id, topic_id = topic_id, question_id = question_id)

    if request.method == 'POST':
        transcript = request.POST.get('transcript', None)
        if request.user.is_authenticated:
            u_id  = request.user.id
            student = Student.objects.get(user_id_login = u_id)

            score = 0

            actual_text = q.question_text
            text_dictionary = {}
            response_dictionary = {}
            total_words = len(actual_text.split())

            # TODO: IMPORT NLTK STOPWORDS

            # creates a hash table using word frequency
            for word in actual_text.split():
                if text_dictionary.get(word) == None:
                    text_dictionary[word] = 1
                else:
                    text_dictionary[word] += 1


            # calculates user score
            for word in transcript.split():
                if text_dictionary.get(word) != None and response_dictionary.get(word) == None:
                    score += text_dictionary[word]

                    # arbitrary value to show the word has been marked
                    response_dictionary[word] = True
                else:
                    pass

            completion = Completion.objects.create(student_id = student, 
                                                   question_id = q, 
                                                   transcript = transcript, 
                                                   percent_scored = score/total_words
                                                   )

            
            completions = Completion.objects.all()


            context = {
                        'q' : q, 
                        'percentage' : str(score/float(total_words)), 
                        'name' : student.f_name,
                        'transcript' : transcript,
                        }
            return render(request, 'review.html', context)

        else:
            pass
                # Redirect to not logged in page


    return render(request, 'speech.html', {'q' : q})


def db(request):

    ## TESTING AREA FOR FUNCTIONS 
    q = Question.objects.all()

    # for qu in q:
    #     try:
    #         print qu.topic_id, " within ", qu.class_id
    #     except:
    #         print "ascii err"

    e = Enrollments.objects.all()

    for i in e:
        print i, i.class_id, i.student_id
#
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

    q = Question.objects.all()

    return render(request, 'db.html', {'t': q})

