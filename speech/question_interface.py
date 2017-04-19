from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import Student, Enrollments, Class, Topic, Question, Teacher, Completion, TopicProgress

from .forms import LoginForm, SignupForm, TeacherSignupForm, TeacherLoginForm

from .data import updateSingleTopicProgress, getPercentString, greatestCompletionByStudent, getClassesOfStudent

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
        print("not authenticated")
        return HttpResponseRedirect('/login')

    studentObj = Student.objects.get(user_id_login = request.user.id)
    classes = getClassesOfStudent(studentObj.student_id)

    return render(request, 'class.html', {'classes': classes})


def topic_page(request, class_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')

    topics = Topic.objects.all().filter(class_id = class_id)
    class_ = Class.objects.get(class_id = class_id)

    #foreach loop to add a field to each topic, giving the percent
    for topic in topics:
        topic.progress = getPercentString(topic.topic_id, request.user.id)

    context = { 'class' : class_,
                'topics' : topics
    }

    return render(request, 'topics.html', context)
    

def question_page(request, class_id, topic_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')
    studentObj = Student.objects.get(user_id_login = request.user.id)
    class_ = Class.objects.get(class_id = class_id)
    topic = Topic.objects.filter(class_id = class_id).filter(topic_id = topic_id).get()
    questions = Question.objects.filter(class_id = class_id).filter(topic_id = topic_id)

    #foreach loop to add student's highest score to each question
    for question in questions:
        question.best = greatestCompletionByStudent(question.question_id, studentObj.student_id)

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

            actual_text = q.question_text

            text_dictionary = {}
            response_dictionary = {}
            total_words = len(actual_text.split())

            # TODO: IMPORT NLTK STOPWORDS

            # creates a hash table using word frequency
            for word in actual_text.split():
                word = word.lower()
                print(word)
                if text_dictionary.get(word) == None:
                    text_dictionary[word] = 1
                else:
                    text_dictionary[word] += 1

            score = 0

            # calculates user score
            for word in transcript.split():
                word = word.lower()
                print(word)
                if text_dictionary.get(word) != None and response_dictionary.get(word) == None:
                    score += text_dictionary[word]

                    # arbitrary value to show the word has been marked
                    response_dictionary[word] = True
                else:
                    pass

            q = Question.objects.get(class_id = class_id, topic_id = topic_id, question_id = question_id)
            student = Student.objects.get(user_id_login = u_id)

            completion = Completion.objects.create(student_id = student, 
                                                   question_id = q, 
                                                   transcript = transcript, 
                                                   percent_scored = float(score)/total_words
                                                   )
            updateSingleTopicProgress(u_id, topic_id)

            result_string = ""
            if float(score)/total_words > q.percent_to_pass:
                result_string = "Pass"
            else: result_string = "Fail"

            context = {
                        'q' : q, 
                        'percentage' : str(100*score/float(total_words)), 
                        'name' : student.f_name,
                        'transcript' : transcript,
                        'result_string' : result_string,
                        'percent_to_pass' : str(100*q.percent_to_pass), 
                        }

            return render(request, 'review.html', context)

        else:
            return HttpResponseRedirect('/login')

    topic = q.topic_id.topic_name
    topic_id = q.topic_id
    class_ = q.class_id

    context = {'q' : q, 
               'topic':topic, 
               'class' : class_, 
               'topic_id' : topic_id
               }

    return render(request, 'speech.html', context)