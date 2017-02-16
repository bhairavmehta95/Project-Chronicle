 # -*- coding: utf-8 -*-
#
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import Student, Enrollments, Class, Topic, Question, Teacher, Completion

from .forms import LoginForm, SignupForm, TeacherSignupForm, TeacherLoginForm, QuestionBuilderForm, QBuilderUpdateForm

from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout

from wiki import wiki_search
from bs4 import BeautifulSoup
import requests
import re
from wiki import search_and_process
import json

import random

def question_builder(request):
    # TODO: Add teacher authentication

    if request.method == 'POST':
        form = QuestionBuilderForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            sources = form.cleaned_data['sources']

            sources_list = sources.split('\n')

            print(sources_list)

            data = {
                'documents' : sources_list,
                'number_of_keywords' : 10
            }

            # r = requests.post('http://0.0.0.0:5000/index', json=data)
            
            # print(r.text)

            form = QBuilderUpdateForm(keywords=10) 
            pass
    else:
        form = QuestionBuilderForm()

    return render(request, 'question_builder.html', {'form' : form})