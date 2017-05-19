from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import Student, Enrollments, Class, Topic, Question, Teacher, Completion, TopicProgress, PrimaryKeyword, SecondaryKeyword

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
        question.percent_to_pass = int(question.percent_to_pass * 100)

    context = {'questions' : questions,
                'class' : class_,
                'topic' : topic,
                }
    return render(request, 'questions.html', context)


def speech(request, class_id, topic_id, question_id):
    if not request.user.is_authenticated:
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
            #
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

def correct(request, classId, topicId, questionId):

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')

    studentObj = Student.objects.get(user_id_login = request.user.id)
    questionObj = Question.objects.get(class_id = classId, topic_id = topicId, question_id = questionId)
    primaryKeywords = PrimaryKeyword.objects.filter(question_id = questionId)
    studentResponse = request.POST['final_transcript']
    keywordDict = {}

    studentScore = 0
    possibleScore = 0

    #add words to dictionary with point values
    for keywordObj in primaryKeywords:
        word = keywordObj.keyword.lower()
        possibleScore += keywordObj.point_value
        if keywordDict.get(word) == None:
            keywordDict[word] = keywordObj.point_value
        else:   # I don't think we should ever have duplicates, but just in case
            keywordDict[word] += keywordObj.point_value

    #studentResponse = re.sub("~!@#$%^&*()_+=-`/*.,[];:'/?><", ' ', studentResponse) #replace illegal characters with a space

    #add student score
    for word in studentResponse.split(' '):
        word = word.lower()
        if keywordDict.get(word) != None:
            studentScore += keywordDict[word]
            keywordDict[word] = 0 #set the point value to 0 bc the points have already been earned

    #create completion object
    completion = Completion.objects.create( student_id = studentObj, 
                                            question_id = questionObj, 
                                            transcript = studentResponse, 
                                            percent_scored = float(studentScore)/possibleScore  )

    #create or update topic progress
    updateSingleTopicProgress(request.user.id, topicId)

    #did the student pass?
    if float(studentScore)/possibleScore > questionObj.percent_to_pass:
        resultString = "Pass"
    else: 
        resultString = "Fail"

    #give the front end neccesary context
    context = {
        'q' : questionObj, 
        'percentage' : str(100*studentScore/possibleScore), 
        'name' : studentObj.f_name,
        'transcript' : studentResponse,
        'result_string' : resultString,
        'percent_to_pass' : str(100*questionObj.percent_to_pass), 
    }

    return context
