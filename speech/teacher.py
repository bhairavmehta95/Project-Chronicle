from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from .models import Student, Enrollments, Class, Topic, Question, Teacher, Keyword

from .forms import LoginForm, SignupForm, TeacherSignupForm, TeacherLoginForm
from .data import updateProgressesFromTopic

from django.contrib.auth.models import User, Group
from .forms import LoginForm, QuestionBuilderForm

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

# Classes
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

def ajaxEditClass(request):
    if (request.method == 'POST'):
        teacherId = getTeacherId(request)
        data = request.POST

        oldClassObj = Class.objects.get(teacher_id = teacherId, class_key = data['classKey'])
        oldClassObj.class_name = data['className']
        oldClassObj.save()
        return HttpResponse(1, content_type="application/json")

def ajaxGetClass(request):
    if (request.method == 'POST'):
        teacherId = getTeacherId(request)
        classKey = request.POST['classKey']
        classObj = Class.objects.get(teacher_id = teacherId, class_key = classKey)
        response = serializers.serialize("json", [classObj])
        return HttpResponse(response, content_type='application/json')

def ajaxDeleteClass(request):
    if (request.method == 'POST'):
        teacherId = getTeacherId(request)
        classKey = request.POST['classKey']
        classObj = Class.objects.get(teacher_id = teacherId, class_key = classKey)
        classObj.delete()
        return HttpResponse(1, content_type='application/json')


# Topics
def addTopic(request):

    if (request.method == 'POST'):
        
        class_key = request.POST['classKey']
        topic_name = request.POST['topicName']
        class_instance = Class.objects.get(class_key = class_key)

        new_topic = Topic.objects.create(class_id=class_instance, topic_name=topic_name)

        response = serializers.serialize("json", [new_topic])
        return HttpResponse(json.dumps(response), content_type='application/json')

    else:
        return HttpResponseRedirect('/')

def getTopics(request, classKey):
    if (request.method == 'GET'):
        teacherId = getTeacherId(request)
        c = Class.objects.get(teacher_id = teacherId, class_key = classKey)
        result = Topic.objects.filter(class_id = c)
        response = serializers.serialize("json", result)
        return HttpResponse(response, content_type='application/json')

def ajaxEditTopic(request):
    if (request.method == 'POST'):
        teacherId = getTeacherId(request)
        data = request.POST
        TopicObj = Topic.objects.get(topic_id = data['topicId'])
        TopicId = TopicObj.topic_id
        if (teacherOwnsTopic(teacherId, TopicId)):
            TopicObj.topic_name = data['topicName']
            TopicObj.save()
            return HttpResponse(1, content_type="application/json")

def ajaxDeleteTopic(request):
    if (request.method == 'POST'):
        teacherId = getTeacherId(request)
        topicId = request.POST['topicId']
        TopicObj = Topic.objects.get(topic_id = topicId)
        TopicId = TopicObj.topic_id
        if (teacherOwnsTopic(teacherId, TopicId)):
            TopicObj.delete()
            return HttpResponse(1, content_type="application/json")


# Questions
def createQuestion(request):
    
    topicId = request.POST['topic']
    title = request.POST['title']
    
    print("topic id " + topicId)
    topic_instance = Topic.objects.get(topic_id = topicId)
    class_instance = topic_instance.class_id

    new_question = Question.objects.create( class_id = class_instance,
                                            topic_id = topic_instance,
                                            question_title = title )
    updateProgressesFromTopic(topicId)
    return HttpResponse(1, content_type='application/json')

def getQuestionsInTopic(request):
    teacherId = getTeacherId(request)
    topicId = request.POST['topicId']
    if (teacherOwnsTopic(teacherId, topicId)):
        result = Question.objects.filter(topic_id = topicId)
        response = serializers.serialize("json", result)
        return HttpResponse(response, content_type='application/json')

def ajaxEditQuestion(request):
    if (request.method == 'POST'):
        teacherId = getTeacherId(request)
        data = request.POST
        QuestionObj = Question.objects.get(topic_id = data['topicId'])
        topicId = QuestionObj.topic_id
        if (teacherOwnsTopic(teacherId, topicId)):
            QuestionObj.question_title = data['quesionTitle']
            QuestionObj.save()
            return HttpResponse(1, content_type="application/json")

def ajaxDeleteQuestion(request):
    if (request.method == 'POST'):
        teacherId = getTeacherId(request)
        data = request.POST
        QuestionObj = Question.objects.get(question_id = data['questionId'])
        topicId = QuestionObj.topic_id.pk
        if (teacherOwnsTopic(teacherId, topicId)):
            QuestionObj.delete()
            return HttpResponse(1, content_type="application/json")


# Keywords
def addKeyword(request):

    questionId = request.POST['questionId']
    questionObj = Question.objects.get( pk = questionId )
    word = request.POST['keyword']
    points = request.POST['points']

    new_keyword = Keyword.objects.create(    question_id = questionObj,
                                                    keyword = word,
                                                    point_value = points    )
    return HttpResponse(1, content_type='application/json')


# Page rendering
def teacher_portal(request):
    if request.method == 'GET':
        teacher = Teacher.objects.filter(user_id_login=request.user.id)
        if (request.user.is_authenticated):
            if teacher.count():
                return render(request, 'teacherportal.html')
            else:
                return HttpResponseRedirect('/classes')
        else:
            signup_form = TeacherSignupForm()
            form = LoginForm()
            return render(request, 'teacherlanding.html', {'form': form, 'signup_form': signup_form})

def teacher_home(request):
    form = QuestionBuilderForm()
    return render(request, 'teacherhome.html', {'form': form })

def classPage(request, classKey):
    t = getTeacherId(request)
    c = Class.objects.get(teacher_id = t, class_key = classKey)
    return render(request, 'teacherclass.html', {'class_name':c, 'class_key':classKey, 'class_id':c.get_class_id()})


# General Functions
def generateClassKey(length):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))

def getTeacherId(request):
    user = request.user.id
    teacher = Teacher.objects.get(user_id_login = user)
    return teacher.get_teacher_id()

def teacherOwnsTopic(teacherId, topicId):
    TopicObj = Topic.objects.get(topic_id = topicId)
    classId = TopicObj.class_id.pk
    ClassQuery = Class.objects.filter(teacher_id = teacherId, class_id = classId)
    return ClassQuery.count