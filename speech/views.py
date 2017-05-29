# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib.auth import authenticate, login, logout

from .models import Student, Enrollments, Class, Teacher
from .forms import LoginForm

import json
import sys
sys.path.insert(0, 'speech/algorithms')


def landing(request):
    return render(request, 'landing.html')


# loads the demo
def demo(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/classes')

    username = 'DEMOUSER'
    password = 'USER$PASSWORD'
    user = authenticate(username=username, password=password)
    
    if user is not None:
        login(request, user)
        return HttpResponseRedirect('/classes')

    return HttpResponseRedirect('/login')


# Create your views here.
def login_user(request):

    error = None

    if request.user.is_authenticated():  # user already logged in
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

            else:  # user exists and is active
                login(request, user)

                if Student.objects.filter(user_id_login=user.id).count():  # this user is a student
                    return HttpResponseRedirect('/classes')

                elif Teacher.objects.filter(user_id_login=user.id).count():  # this user is a teacher
                    return HttpResponseRedirect('/teacher')

    form = LoginForm()
    return render(request, 'login.html', {'error': error, 'form': form})


def logout_user(request):
    if request.user.is_authenticated():
        logout(request)
        return HttpResponseRedirect('/login')
    
    return HttpResponseRedirect('/classes')


def about(request):
    return render(request, 'about.html')


def enroll(request):

    if request.user.is_authenticated():
        student_obj = Student.objects.get(user_id_login=request.user.id)
        class_obj = Class.objects.get(class_key=request.POST['classKey'])

        new_enrollment = Enrollments.objects.create(student_id=student_obj, class_id=class_obj)
        response = serializers.serialize("json", [new_enrollment])
        return HttpResponse(json.dumps(response), content_type='application/json')
    else:
        return HttpResponseRedirect('/')
