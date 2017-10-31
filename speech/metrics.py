# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers

from .models import Student, Enrollments, Class, Teacher

import json
import sys

def metrics(request):
    if not request.user.is_authenticated(): # Not logged in
        return HttpResponseRedirect('/login')

    elif Teacher.objects.filter(user_id_login = request.user.id).count: # Teacher
        return render(request, 'teacher_metrics.html')

    else: # Student
        return HttpResponseRedirect('/classes')

def getStudentPerformance(request):
    teacher = Teacher.objects.get(user_id_login = request.user.id)
    classes = Class.objects.filter(teacher_id = teacher)
    enrollments = list()
    studentPerformances = {}
    for idx, obj in enumerate(classes):
        for idx2, obj2 in enumerate(Enrollments.objects.filter(class_id = obj.pk)):
            enrollments.append(obj2)
    for idx, performance in enumerate(enrollments):
        # completions = getCompletions(performance.class_id.pk, performance.student_id.pk)
        studentPerformances[idx] = {
            'class': performance.class_id.__str__(),
            'user': performance.student_id.f_name + ' ' + performance.student_id.l_name,
            'questions_attempted': performance.student_id.Completions.count
            # 'average_score': 0,
            # 'best_score': 0
        }
    return JsonResponse(studentPerformances)