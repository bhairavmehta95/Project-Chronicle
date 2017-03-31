from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from .models import Student, Enrollments, Class, Topic, Question, Teacher, Completion

from .forms import LoginForm, SignupForm, TeacherSignupForm, TeacherLoginForm

from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout

from wiki import wiki_search
from bs4 import BeautifulSoup
import requests
import re
from wiki import search_and_process
import json
from django.core import serializers

import random
import string

def signup_teacher(request):
    # if this is a POST request we need to process the form data
    error = None
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TeacherSignupForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']
            retyped = form.cleaned_data['retyped']
            teacher_id = form.cleaned_data['teacher_id']
            #class_name = form.cleaned_data['class_name']

            # Password Checking
            if (password != retyped):
                error = "Passwords don't match"

            if error == None:
                user = User.objects.create_user(username=username,
                                        email = email,
                                        password=password)

                try:
                    group = Group.objects.get(name = "teacher")
                except:
                    group = Group.objects.create(name = "teacher")

                t = Teacher.objects.create(user_id_login = user.id, f_name = first_name, l_name = last_name, teacher_id = teacher_id)
                #c = Class.objects.create(teacher_id = t, class_name = class_name)

                user.groups.add(group)

                return HttpResponseRedirect('/teacher')

    # if a GET (or any other method) we'll create a blank form
    form = TeacherSignupForm();
    return render(request, 'teachersignup.html', {'form': form, 'error' : error, })

def teacher_portal(request):
    if request.method == 'GET':
        if (request.user.is_authenticated and not request.user.has_perm("speech.add_class")):
            return HttpResponseRedirect('/classes')
        elif (request.user.is_authenticated and request.user.has_perm("speech.add_class")):
            return render(request, 'teacherportal.html')
        else:
            return render(request, 'teacherlanding.html')

def createClass(request):
    if (request.method == 'POST'):
        user = request.user.id
        teacher = Teacher.objects.get(user_id_login = user)
        teacher_id = teacher.get_teacher_id()
        key = generateClassKey(6)
        class_result = Class.objects.create(teacher_id=Teacher.objects.get(pk=teacher_id), class_name=request.POST['className'], class_key=key)
        response = serializers.serialize("json", [class_result])
        return HttpResponse(json.dumps(response), content_type='application/json')
    else:
        return HttpResponseRedirect('/')

def getClasses(request):
    if (request.method == 'GET'):
        t = getTeacherId(request)
        c = Class.objects.filter(teacher_id = t)
        response = serializers.serialize("json", c)
        return HttpResponse(response, content_type='application/json')

def getTopics(request, classKey):
    if (request.method == 'GET'):
        teacherId = getTeacherId(request)
        if (teacherOwnsClass(teacherId, classKey)):
            c = Class.objects.get(class_key = classKey)
            result = Topic.objects.filter(class_id = c)
            response = serializers.serialize("json", result)
            return HttpResponse(response, content_type='application/json')

def classPage(request, classKey):
    t = getTeacherId(request)
    c = Class.objects.get(teacher_id = t, class_key = classKey)
    return render(request, 'teacherclass.html', {'class_name':c, 'class_key':classKey, 'class_id':c.get_class_id()})

def addTopic(request):

    if (request.method == 'POST'):
        
        class_id = request.POST['classId']
        topic_name = request.POST['topicName']
        class_instance = Class.objects.get(class_id = class_id)

        new_topic = Topic.objects.create(class_id=class_instance, topic_name=topic_name)

        response = serializers.serialize("json", [new_topic])
        return HttpResponse(json.dumps(response), content_type='application/json')

    else:
        return HttpResponseRedirect('/')

def createQuestion(request):
    
    topicId = request.POST['topic']
    title = request.POST['title']
    words = request.POST['words']
    
    topic_instance = Topic.objects.get(topic_id = topicId)
    class_instance = topic_instance.class_id

    new_question = Question.objects.create( class_id = class_instance,
                                            topic_id = topic_instance,
                                            question_subject = title,
                                            question_text = words)


# General Functions
def generateClassKey(length):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))

def getTeacherId(request):
    user = request.user.id
    teacher = Teacher.objects.get(user_id_login = user)
    return teacher.get_teacher_id()

def teacherOwnsClass(teacherId, classKey):
    result = Class.objects.filter(teacher_id = teacherId, class_key = classKey)
    return result.count() == 1