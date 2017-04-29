 # -*- coding: utf-8 -*-
#
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import Student, Enrollments, Class, Topic, Question, Completion, Teacher, PrimaryKeyword, SecondaryKeyword

from .forms import LoginForm, SignupForm, TeacherSignupForm, TeacherLoginForm, QuestionBuilderForm, QBuilderUpdateForm,  \
IntegerValidatorForm, StringValidatorForm

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
    if request.method == 'POST':
        builder_form = QuestionBuilderForm(request.POST)

        # Question Update Form was submitted, time to validate
        if not builder_form.is_valid() and request.POST.get('is_qbuilder_update'):
            data = []
            test_form = None
            error = False
            
            test_form = IntegerValidatorForm(data={'integer' :request.POST.get('number_of_keywords')})
            
            if test_form.is_valid():
                number_of_keywords = test_form.cleaned_data.get('integer')
            else:
                error = True
            
            test_form = StringValidatorForm(data={'string' : request.POST.get('question_title') })

            if test_form.is_valid():
                question_title = test_form.cleaned_data.get('string')
            else:
                error = True

            if not error:
                for index in range(int(number_of_keywords)):
                    # generate extra fields in the number specified via extra_fields
                    test_form = StringValidatorForm(data = {'string' : request.POST.get('keyword_field_{index}'.format(index=index)) } )

                    if test_form.is_valid():
                        keyword = test_form.cleaned_data.get('string')
                    else:
                        error = True
                        break

                    test_form = IntegerValidatorForm(data = {'integer' : request.POST.get('keyword_point_field_{index}'.format(index=index)) } )

                    if test_form.is_valid():
                        points = test_form.cleaned_data.get('integer')
                    else:
                        error = True
                        break

                    data.append((keyword, points))

                # End Vallidation
                if error:
                    return 

        # check whether a builder form was submitted and if it is valid:
        if builder_form.is_valid():
            sources = builder_form.cleaned_data['sources']
            q_title = builder_form.cleaned_data['question_title']
            number_of_keywords = builder_form.cleaned_data['keywords_to_return']
            
            sources_list = sources.split('\n')

            data = {
                'documents': sources_list,
                'num_primary_keywords': number_of_keywords,
                'num_secondary_keywords':int(number_of_keywords / 2)
            }

            r = requests.post('http://pc-api-secretbuilder.us-west-2.elasticbeanstalk.com', json=data)
            print(r.text)
            response_json = json.loads(r.text)

            form_fields = {}

            form_fields['question_title'] = q_title

            for idx, word in enumerate(response_json['words']):
                form_fields['keyword_field_{index}'.format(index=idx)] = response_json['words'][idx]
                form_fields['keyword_point_field_{index}'.format(index=idx)] = response_json['point_values'][idx]

            update_form = QBuilderUpdateForm()
            form = QBuilderUpdateForm.empty_init(update_form, keywords=number_of_keywords, data=form_fields)
            
    else:
        form = QuestionBuilderForm()

    return render(request, 'question_builder.html', {'form' : form})

def points_validator(point_value):
    return is_instance(point_value)

# def addQuestion(request):
#