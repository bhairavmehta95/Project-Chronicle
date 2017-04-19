 # -*- coding: utf-8 -*-
#

import sys
sys.path.insert(0, 'speech/algorithms');

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import Student, Enrollments, Class, Topic, Question, Teacher, Completion

from .forms import LoginForm, SignupForm, TeacherSignupForm, TeacherLoginForm

from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout

#from speech.algorithms.wiki import wiki_search
from bs4 import BeautifulSoup
import requests
import re
#from wiki import search_and_process
import json
from django.core import serializers

import random

def landing(request):
    return render(request, 'landing.html')

# loads the demo
def demo(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/classes')

    username = 'DEMOUSER'
    password = 'USER$PASSWORD'
    user = authenticate(username=username, password=password)
    
    if user != None:
        login(request, user)
        return HttpResponseRedirect('/classes')

    return HttpResponseRedirect('/login')


# Create your views here.
def login_user(request):

    error = None

    if request.user.is_authenticated(): #user already logged in
        
        return HttpResponseRedirect('/classes')
        
    if request.method == 'POST':
        
        form = LoginForm(request.POST)
        
        if form.is_valid():
            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is None:
                
                error = "Not a valid username or password, please try again."
            
            elif not user.is_active:

                error = "Disabled account, contact sysadmin"

            else: #user exists and is active

                login(request, user)

                if Student.objects.filter(user_id_login = user.id).count(): #this user is a student

                    return HttpResponseRedirect('/classes')

                elif Teacher.objects.filter(user_id_login = user.id).count(): #this user is a teacher

                    return HttpResponseRedirect('/teacher')

    form = LoginForm()
    return render(request, 'login.html', { 'error' : error, 'form': form})

def logout_user(request):
    if request.user.is_authenticated():
        logout(request)
        return HttpResponseRedirect('/login')
    
    return HttpResponseRedirect('/classes')

def about(request):
    return render(request, 'about.html')

def enroll(request):

    if request.user.is_authenticated():
        
        studentObj = Student.objects.get(user_id_login = request.user.id)
        classObj = Class.objects.get(class_key = request.POST['classKey'])

        newEnrollment = Enrollments.objects.create(student_id = studentObj, class_id = classObj)
        response = serializers.serialize("json", [newEnrollment])
        return HttpResponse(json.dumps(response), content_type='application/json')

    else:

        return HttpResponseRedirect('/')

def db(request):

#     ## TESTING AREA FOR FUNCTIONS 
    q = Question.objects.all()

    # for qu in q:
    #     try:
    #         print qu.topic_id, " within ", qu.class_id
    #     except:
    #         print "ascii err"

#     e = Enrollments.objects.all()

#     for i in e:
#         print i, i.class_id, i.student_id
# #
#     return render(request, 'db.html', {'t': q})

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

        # makes sure URL has not been checked
        if url.find('%') != -1 and url.find('#') == -1 and not url in url_list:
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

