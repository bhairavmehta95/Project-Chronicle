# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Class, Topic, Question, Keyword, RawText, KeywordContext
from .forms import QuestionBuilderForm, QBuilderUpdateForm, IntegerValidatorForm, StringValidatorForm

import requests
import json
import re
from math import ceil


def question_builder(request, class_id, topic_id):
    class_ = Class.objects.get(class_id=class_id)
    topic_ = Topic.objects.get(topic_id=topic_id)
    form = QuestionBuilderForm()

    if class_ is None or topic_ is None:
        # TODO
        print("error should go here")

    if request.method == 'POST':
        builder_form = QuestionBuilderForm(request.POST)
        print(request.POST.get('is_qbuilder_update'))

        # Question Update Form was submitted, time to validate
        if not builder_form.is_valid() and request.POST.get('is_qbuilder_update'):

            num_keywords, question_title, primary_data, secondary_data, raw_text, error = \
                verify_question_update_form(request.POST)

            if error:
                request.method = 'GET'
                return HttpResponseRedirect('/builder/{}/{}'.format(class_id, topic_id))

            # Add question to database
            question_ = Question.objects.create(class_id=class_, topic_id=topic_, question_title=question_title)

            RawText.objects.create(question_id=question_, raw_text=raw_text)

            raw_text_list = raw_text.lower().split()
            raw_text_list[:] = [re.sub(r'[^a-zA-Z0-9]+', '', word) for word in raw_text_list]

            for kw_tuple in primary_data:
                kw = Keyword.objects.create(question_id=question_, keyword=kw_tuple[0],
                                            point_value=float(kw_tuple[1]), is_primary=True)
                word = kw_tuple[0]

                context_index = raw_text_list.index(word)
                context = ""

                i = 5
                while (i > 0):
                    try:
                        context = context + raw_text_list[context_index - i] + " "
                        i -= 1
                    except:
                        break

                print word, context
                KeywordContext.objects.create(question_id=question_, keyword=kw, context=context, previous=True)

                context = ""
                i = 1
                while (i < 6):
                    try:
                        context = context + raw_text_list[context_index + i] + " "
                        i += 1
                    except:
                        break

                print word, context
                KeywordContext.objects.create(question_id=question_, keyword=kw, context=context, previous=False)

            for kw_tuple in secondary_data:
                Keyword.objects.create(question_id=question_, keyword=kw_tuple[0],
                                       point_value=float(kw_tuple[1]), is_primary=False)

            request.method = 'GET'
            return HttpResponseRedirect('/builder/{}/{}'.format(class_id, topic_id))

        # check whether a builder form was submitted and if it is valid:
        if builder_form.is_valid():
            sources = builder_form.cleaned_data['sources']
            q_title = builder_form.cleaned_data['question_title']
            num_keywords = builder_form.cleaned_data['keywords_to_return']

            sources_list = [s.strip() for s in sources.splitlines()]
            sources_list = filter(lambda a: a != '', sources_list)

            data = {
                'documents': sources_list,
                'num_primary_keywords': num_keywords,
                'num_secondary_keywords': int(ceil(num_keywords / 2))
            }

            # keyword api
            r = requests.post('http://pc-builder-dev2.us-west-2.elasticbeanstalk.com/index', json=data)
            # r = requests.post('http://0.0.0.0:5000/index', json=data)
            response_json = json.loads(r.text)

            form_fields = dict()

            form_fields['question_title'] = q_title
            form_fields['raw_text'] = response_json['raw_text']

            for idx, word in enumerate(response_json['primary_words']):
                form_fields['primary_keyword_field_{index}'.format(index=idx)] = response_json['primary_words'][idx]
                form_fields['primary_keyword_point_field_{index}'.format(index=idx)] = \
                    response_json['primary_point_values'][idx]

            for idx, word in enumerate(response_json['secondary_words']):
                form_fields['secondary_keyword_field_{index}'.format(index=idx)] = response_json['secondary_words'][idx]
                form_fields['secondary_keyword_point_field_{index}'.format(index=idx)] = \
                    response_json['secondary_point_values'][idx]

            update_form = QBuilderUpdateForm()
            form = QBuilderUpdateForm.empty_init(
                update_form,
                primary_keywords=len(response_json['primary_words']),
                secondary_keywords=len(response_json['secondary_words']),
                data=form_fields
            )

            return render(request, 'question_builder_post.html', {'form': form, 'q_title': q_title  })

    return render(request, 'question_builder.html', {'form': form})


def verify_question_update_form(post_data):
    primary_data = []
    secondary_data = []
    error = False
    test_form = IntegerValidatorForm(data={'integer': post_data.get('num_primary_keywords')})

    if test_form.is_valid():
        num_primary_keywords = test_form.cleaned_data.get('integer')
    else:
        error = True

    test_form = StringValidatorForm(data={'string': post_data.get('question_title')})

    if test_form.is_valid():
        question_title = test_form.cleaned_data.get('string')
    else:
        error = True

    test_form = StringValidatorForm(data={'string': post_data.get('raw_text')})

    if test_form.is_valid():
        raw_text = test_form.cleaned_data.get('string')
    else:
        error = True

    if not error:
        for index in range(int(num_primary_keywords)):
            # generate extra fields in the number specified via extra_fields
            test_form = StringValidatorForm(data={'string': post_data.get(
                'primary_keyword_field_{index}'.format(index=index))})

            if test_form.is_valid():
                keyword = test_form.cleaned_data.get('string')
            else:
                error = True
                break

            test_form = IntegerValidatorForm(
                data={'integer': post_data.get('primary_keyword_point_field_{index}'.format(index=index))})

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

        return num_primary_keywords + int(num_secondary_keywords), question_title, primary_data, \
               secondary_data, raw_text, error

    # Return an error
    return None, None, None, None, None, error