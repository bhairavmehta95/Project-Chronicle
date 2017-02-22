from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

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

import random

def signup_user(request):
    # if this is a POST request we need to process the form data
    error = None
    if request.method == 'POST':
        print("got the post");
        # create a form instance and populate it with data from the request:
        form = SignupForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            print("form is valid");
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']
            retyped = form.cleaned_data['retyped']
            #teacher_id = form.cleaned_data['teacher_id']

            # Password Checking
            if (password != retyped):
                error = "Passwords don't match."

            # Password Length: TODO - replace with django validators
            if len(password) < 8 or len(username) < 8:
                error = "Username and password must be more than eight characters."

            # Check existing user
            try:
                user = User.objects.get(username=username)
                error = "Username already exists in system."
            except:
                pass

            #class_id = request.POST['Class']

            # TODO: ONLY SHOW THE CLASSES CORRESPONDING TO A SPECIFIC TEACHER
            # teacher_target = Class.objects.get(class_id = class_id).teacher_id

            # if teacher_target.teacher_id != teacher_id:
            #     error = "Please pick a real teacher/class pair, this is only temporary"

            print("here's what's in error:");
            print(error);
            if error == None:
                class_target = Class.objects.get(class_id = class_id)

                user = User.objects.create_user(username=username,
                                    email = email,
                                    password=password)

                try:
                    group = Group.objects.get(name = "student")
                except:
                    group = Group.objects.create(name = "student")

                s = Student.objects.create(user_id_login = user.id, f_name = first_name, l_name = last_name)
                
                user.groups.add(group)

                Enrollments.objects.create(student_id = s, class_id = class_target)

                print "Welcome", s, "please login"
                return HttpResponseRedirect('/login')
            

    # if a GET (or any other method) we'll create a blank form
    classes = Class.objects.all()
    form = SignupForm()

    return render(request, 'signup.html', {'form': form, 'classes' : classes, 'error' : error, })

def login_user(request):

    # user already logged in, take them to classes
    if request.user.is_authenticated():
        return HttpResponseRedirect('/classes')
        
    # if this is a POST request we need to process the form data
    error = None
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(form.cleaned_data['username'])
            print(form.cleaned_data['password'])
            user = authenticate(username=username, password=password)
            print("Authenticate executed.")
            print(user);
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

def logout_user(request):
    if request.user.is_authenticated():
        logout(request)
        return HttpResponseRedirect('/login')
    
    return HttpResponseRedirect('/classes')