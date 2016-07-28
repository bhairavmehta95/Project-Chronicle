from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting, Student, Enrollment, Class, Topic, Question

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')


def db(request):

    # greeting = Greeting()
    # greeting.save()

    # greetings = Greeting.objects.all()

    s = Student(student_id = 1, f_name = "bhairav", l_name = "mehta")

    s.save()

    students = Student.objects.all()

    return render(request, 'db.html', {'students': students})

