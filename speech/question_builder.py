 # -*- coding: utf-8 -*-
#
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import Student, Enrollments, Class, Topic, Question, Completion, Teacher, PrimaryKeyword, SecondaryKeyword

from .forms import LoginForm, SignupForm, TeacherSignupForm, TeacherLoginForm, QuestionBuilderForm, QBuilderUpdateForm,  \
IntegerValidatorForm, StringValidatorForm

from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout

import requests
import re
import json

from math import ceil


def question_builder(request, class_id, topic_id):
    class_ = Class.objects.get(class_id=class_id)
    topic_ = Topic.objects.get(topic_id=topic_id)

    if class_ == None or topic_ == None:
        return "error should go here"

    if request.method == 'POST':
        builder_form = QuestionBuilderForm(request.POST)

        # Question Update Form was submitted, time to validate
        if not builder_form.is_valid() and request.POST.get('is_qbuilder_update'):
            num_keywords, question_title, primary_data, secondary_data, error = verify_question_update_form(request.POST)

            # Add question to database
            question_ = Question.objects.create(class_id=class_, topic_id=topic_, question_title=question_title)

            for kw_tuple in primary_data:
                primary_keyword = PrimaryKeyword.objects.create(question_id=question_, keyword=kw_tuple[0], point_value=kw_tuple[1])

            for kw_tuple in secondary_data:
                secondary_keyword = SecondaryKeyword.objects.create(question_id=question_, keyword=kw_tuple[0], point_value=kw_tuple[1])                

            # TODO: Add redirect

            return "Success!"


        # check whether a builder form was submitted and if it is valid:
        if builder_form.is_valid():
            sources = builder_form.cleaned_data['sources']
            q_title = builder_form.cleaned_data['question_title']
            num_keywords = builder_form.cleaned_data['keywords_to_return']

            sources_list = sources.split('\n')

            data = {
                'documents' : sources_list,
                'num_primary_keywords' : num_keywords,
                'num_secondary_keywords' : int(ceil(num_keywords / 2))
            }
            
            # indexer api
            # r = requests.post('http://0.0.0.0:6000/index', json=data)
            
            # keyword api
            r = requests.post('http://0.0.0.0:5000/index', json=data)
            response_json = json.loads(r.text)
 
            form_fields = {}

            form_fields['question_title'] = q_title

            for idx, word in enumerate(response_json['primary_words']):
                form_fields['primary_keyword_field_{index}'.format(index=idx)] = response_json['primary_words'][idx]
                form_fields['primary_keyword_point_field_{index}'.format(index=idx)] = response_json['primary_point_values'][idx]

            for idx, word in enumerate(response_json['secondary_words']):
                form_fields['secondary_keyword_field_{index}'.format(index=idx)] = response_json['secondary_words'][idx]
                form_fields['secondary_keyword_point_field_{index}'.format(index=idx)] = response_json['secondary_point_values'][idx]

            update_form = QBuilderUpdateForm()
            form = QBuilderUpdateForm.empty_init(
                    update_form, 
                    primary_keywords=len(response_json['primary_words']), 
                    secondary_keywords=len(response_json['secondary_words']), 
                    data=form_fields
                    )
            
    else:
        form = QuestionBuilderForm()

    return render(request, 'question_builder.html', {'form' : form})

def verify_question_update_form(post_data):
    primary_data = []
    secondary_data = []
    test_form = None
    error = False
    
    test_form = IntegerValidatorForm(data={'integer' :post_data.get('num_primary_keywords')})
    
    if test_form.is_valid():
        num_primary_keywords = test_form.cleaned_data.get('integer')
    else:
        error = True
    
    test_form = StringValidatorForm(data = {'string' : post_data.get('question_title') })

    if test_form.is_valid():
        question_title = test_form.cleaned_data.get('string')
    else:
        error = True

    if not error:
        for index in range(int(num_primary_keywords)):
            # generate extra fields in the number specified via extra_fields
            test_form = StringValidatorForm(data = {'string' : post_data.get('primary_keyword_field_{index}'.format(index=index)) } )

            if test_form.is_valid():
                keyword = test_form.cleaned_data.get('string')
            else:
                error = True
                break

            test_form = IntegerValidatorForm(data = {'integer' : post_data.get('primary_keyword_point_field_{index}'.format(index=index)) } )

            if test_form.is_valid():
                points = test_form.cleaned_data.get('integer')
            else:
                error = True
                break

            primary_data.append((keyword, points))

        num_secondary_keywords = post_data.get('num_secondary_keywords')
        for index in range(int(num_secondary_keywords)):
            kw = post_data.get('secondary_keyword_field_{index}'.format(index=index))
            point_value = post_data.get('secondary_keyword_point_field_{index}'.format(index=index))
            secondary_data.append((kw, point_value))


    return num_primary_keywords + int(num_secondary_keywords), question_title, primary_data, secondary_data, error