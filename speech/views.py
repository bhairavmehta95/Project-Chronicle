from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting, Student, Enrollments, Class, Topic, Question

from .forms import SignupForm

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = SignupForm()
        return render(request, 'signup.html', {'form': form})

    return render(request, 'index.html')

def signup_user(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SignupForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            f_name_new = form.cleaned_data['f_name']
            l_name_new = form.cleaned_data['l_name']

            # TO DO: Check the user information before adding
            # TO DO: Autoincrement student_id
            # TO DO: Add email and password?

            s = Student(student_id = 1, f_name = f_name_new, l_name = l_name_new)
            s.save()

            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            print "Thanks!"
            return render(request, 'index.html')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})

def class_page(request):
    classes = Class.objects.all()
    if (request.method == 'POST'):
        class_name = request.POST['Class']
        class_ = Class.objects.filter(class_name=class_name)
        class_id = class_[0].get_class_id()

        topics = Topic.objects.filter(class_id=class_id)

        # TO DO: How to configure the URL the right way, currently passes in correct topics
        return render(request, 'topics.html', {'topics' : topics})

    return render(request, 'class.html', {'classes': classes})

def topic_page(request):
    pass
    

def question_page(request):
    pass

def db(request):

    # greeting = Greeting()
    # greeting.save()

    # greetings = Greeting.objects.all()

    # s = Student(student_id = 1, f_name = "bhairav", l_name = "mehta")

    # s.save()

    students = Student.objects.all()

    return render(request, 'db.html', {'students': students})

