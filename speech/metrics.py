# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers

from .models import Student, Enrollments, Class, Teacher, Completion, Question

import json
import sys

def metrics(request):
    if not request.user.is_authenticated(): # Not logged in
        return HttpResponseRedirect('/login')

    elif request.user.groups.filter(name='teacher').exists(): # Teacher
        return render(request, 'teacher_metrics.html')

    else: # Student
        return render(request, 'message.html', { 'title': 'Oops!', 'message': 'Unfortunately, we haven\'t implemented this feature for students yet. This is currently in development and a high priority at Project Chronicle. Check back later!' })

def get_student_performance(request):
    teacher = Teacher.objects.get(user_id_login = request.user.id)
    classes = Class.objects.filter(teacher_id = teacher)
    enrollments = list()
    studentPerformances = {}
    for idx, obj in enumerate(classes):
        for idx2, obj2 in enumerate(Enrollments.objects.filter(class_id = obj.pk)):
            enrollments.append(obj2)
    for idx, enrollment in enumerate(enrollments):
        completions = get_completions(enrollment.student_id.pk, enrollment.class_id.pk)
        studentPerformances[idx] = {
            'class_name': enrollment.class_id.__str__(),
            'student_name': enrollment.student_id.f_name + ' ' + enrollment.student_id.l_name,
            'total_responses': len(completions),
            'questions_attempted': get_num_question_attempts(completions),
            'questions_passed': get_num_questions_passed(completions),
        }
    return JsonResponse(studentPerformances)

def get_completions(student_id, class_id):
    all_completions = Completion.objects.filter(student_id=student_id)
    relevant_completions = list()
    for index, completion in enumerate(all_completions):
        if (completion.question_id.topic_id.class_id.pk == class_id):
            relevant_completions.append(completion)
    return relevant_completions

def get_num_question_attempts(completionList):
    questions_attempted = {}
    for index, completion in enumerate(completionList):
        if (questions_attempted.get(completion.question_id) is None):
            questions_attempted[completion.question_id] = 1
    return len(questions_attempted)

def get_num_questions_passed(completionList):
    questions_attempted = {}
    for index, completion in enumerate(completionList):
        if (completion.percent_scored >= completion.question_id.percent_to_pass and questions_attempted.get(completion.question_id) is None):
            questions_attempted[completion.question_id] = 1
    return len(questions_attempted)

def get_question_statistics(request):
    questions = Question.objects.filter(class_id__teacher_id__user_id_login=request.user.id)
    question_statistics = {}
    for index, question in enumerate(questions):
        responses = Completion.objects.filter(question_id = question.pk)
        question_statistics[index] = {
            'question_name': question.question_title,
            'num_responses': len(responses),
            'num_passed'   : get_num_passed(responses),
            'average_score': get_average_score(responses)
        }
    return JsonResponse(question_statistics)

def get_num_passed(responses):
    number = 0
    for index, response in enumerate(responses):
        if (response.percent_scored >= response.question_id.percent_to_pass):
            number += 1
    return number

def get_average_score(responses):
    if (len(responses) < 1):
        return 0
    else:
        sum = 0
        for index, response in enumerate(responses):
            sum += response.percent_scored
        return round(sum / len(responses) * 1000) / 10