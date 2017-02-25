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
            q_title = form.cleaned_data['question_title']
            number_of_keywords = form.cleaned_data['keywords_to_return']
            
            sources_list = sources.split('\n')

            data = {
                'documents' : sources_list,
                'number_of_keywords' : number_of_keywords
            }

            r = requests.post('http://0.0.0.0:5000/index', json=data)
            response_json = json.loads(r.text)
 
                
            form_fields = {}

            form_fields['question_title'] = q_title

            for idx, word in enumerate(response_json['words']):
                form_fields['keyword_field_{index}'.format(index=idx)] = response_json['words'][idx]
                form_fields['keyword_point_field_{index}'.format(index=idx)] = response_json['point_values'][idx]

            form = QBuilderUpdateForm(keywords=number_of_keywords, data=form_fields)

            print(form.fields)
            
    else:
        form = QuestionBuilderForm()

    return render(request, 'question_builder.html', {'form' : form})