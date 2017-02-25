from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import Student, Enrollments, Class, Topic, Question, Teacher, Completion, Instructor

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
                    group = Group.objects.get(name = "instructor")
                except:
                    group = Group.objects.create(name = "instructor")

                t = Teacher.objects.create(user_id_login = user.id, f_name = first_name, l_name = last_name, teacher_id = teacher_id);
                #c = Class.objects.create(teacher_id = t, class_name = class_name)

                user.groups.add(group)


                print "Welcome", t, "please login"
                return HttpResponseRedirect('/teacher')

    # if a GET (or any other method) we'll create a blank form
    form = TeacherSignupForm();
    return render(request, 'teachersignup.html', {'form': form, 'error' : error, })

def login_teacher(request):
    # if this is a POST request we need to process the form data
    error = None
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TeacherLoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            # TO DO: Check the user is a TEACHER (check above as well)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    t = Teacher.objects.get(user_id_login = user.id)
                    print "Welcome back: ", t
                    # Redirect to a success page.
                    return HttpResponseRedirect('/classes')
                else:
                    error = "Disabled account, contact sysadmin"
                    # Return a 'disabled account' error message
            else:
                error = "Not a valid username or password, please try again."

            return render(request, 'teacher.html', { 'error' : error, 'form': form})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TeacherLoginForm()

    return render(request, 'teacher.html', {'form': form})