from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import Student, Enrollments, Class, Topic, Question, Teacher, Completion, PrimaryKeyword, SecondaryKeyword

from .forms import LoginForm, SignupForm, TeacherSignupForm, TeacherLoginForm

from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout

from wiki import wiki_search
from bs4 import BeautifulSoup
import requests
import re
from wiki import search_and_process
import json

import random

def class_page(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')

    classes = Class.objects.all()
    return render(request, 'class.html', {'classes': classes})

def topic_page(request, class_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')

    topics = Topic.objects.all().filter(class_id = class_id)
    class_ = Class.objects.get(class_id = class_id)
    context = { 'class' : class_,
                'topics' : topics
    }

    return render(request, 'topics.html', context)
    

def question_page(request, class_id, topic_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')
    class_ = Class.objects.get(class_id = class_id)
    topic = Topic.objects.filter(class_id = class_id).filter(topic_id = topic_id).get()
    questions = Question.objects.filter(class_id = class_id).filter(topic_id = topic_id)
    context = {'questions' : questions,
                'class' : class_,
                'topic' : topic,
                }
    return render(request, 'questions.html', context)


def speech(request, class_id, topic_id, question_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')

    q = Question.objects.get(class_id = class_id, topic_id = topic_id, question_id = question_id)

    if request.method == 'POST':
        transcript = request.POST.get('final_transcript', None)
        if request.user.is_authenticated:
            u_id  = request.user.id
            student = Student.objects.get(user_id_login = u_id)

            score = 0

            context = calculateScore(q, transcript)

            return render(request, 'review.html', context)

        else:
            pass
                # Redirect to not logged in page

    topic = q.topic_id.topic_name
    topic_id = q.topic_id
    class_ = q.class_id

    context = {'q' : q, 
               'topic':topic, 
               'class' : class_, 
               'topic_id' : topic_id
               }

    return render(request, 'speech.html', context)


def calculateScore(question_, transcript):
    primary_keywords = PrimaryKeyword.objects.all().filter(question_id=question_)
    secondary_keywords = SecondaryKeyword.objects.all().filter(question_id=question_)

    total_points_available = 0
    user_points = 0

    # TODO: IMPORT NLTK STOPWORDS

    score_dict = {}
    for element in primary_keywords:
        kw = element.keyword
        points = element.point_value

        score_dict[kw] = points

        total_points_available += points

    for element in secondary_keywords:
        kw = element.keyword
        points = element.point_value

        score_dict[kw] = points

        total_points_available += points

    for word in transcript.split():
        if word in score_dict:
            user_points += score_dict[word]


    # TODO: Add multipliers, teacher answer queries, etc.

    completion = Completion.objects.create(
                               student_id = student, 
                               question_id = question_, 
                               transcript = transcript, 
                               percent_scored = user_points/float(total_points_available)
                               )

    result_string = ""
    print score/total_words, q.percent_to_pass, score/total_words > q.percent_to_pass 
    if score/total_words > q.percent_to_pass:
        result_string = "Pass"
    else: result_string = "Fail"

    context = {
                'q' : q, 
                'percentage' : str(100*user_points/float(total_points_available)), 
                'name' : student.f_name,
                'transcript' : transcript,
                'result_string' : result_string,
                'percent_to_pass' : str(100*q.percent_to_pass), 
                }