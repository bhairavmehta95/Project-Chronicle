from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting, Student, Enrollments, Class, Topic, Question

from .forms import SignupForm

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    if request.method == 'POST':
    	return render(request, 'signup.html')

    return render(request, 'speech.html')

def signup_user(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SignupForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            print "Thanks!"
            return render(request, 'index.html')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'signup.html', {'form': form})


def db(request):

    # greeting = Greeting()
    # greeting.save()

    # greetings = Greeting.objects.all()

    s = Student(student_id = 1, f_name = "bhairav", l_name = "mehta")

    s.save()

    students = Student.objects.all()

    return render(request, 'db.html', {'students': students})

