from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import Student, Class
from .forms import SignupForm

from django.contrib.auth.models import User, Group
from django.contrib.auth import logout
e
def signup_user(request):
    # if this is a POST request we need to process the form data
    error = None
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SignupForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']
            retyped = form.cleaned_data['retyped']

            # Password Checking
            if password != retyped:
                error = "Passwords don't match."

            # Password Length: TODO - replace with django validators
            if len(password) < 8 or len(username) < 8:
                error = "Username and password must be more than eight characters."

            # Check existing user
            try:
                User.objects.get(username=username)
                error = "Username already exists in system."
            except:
                pass

            # TODO: ONLY SHOW THE CLASSES CORRESPONDING TO A SPECIFIC TEACHER
            # teacher_target = Class.objects.get(class_id = class_id).teacher_id

            # if teacher_target.teacher_id != teacher_id:
            #     error = "Please pick a real teacher/class pair, this is only temporary"

            print("here's what's in error:")
            print(error)

            if error is None:

                user = User.objects.create_user(username=username,
                                                email=email,
                                                password=password)

                try:
                    group = Group.objects.get(name="student")
                except:
                    group = Group.objects.create(name="student")

                Student.objects.create(user_id_login=user.id, f_name=first_name, l_name=last_name)
                user.groups.add(group)

                return HttpResponseRedirect('/login')

    # if a GET (or any other method) we'll create a blank form
    classes = Class.objects.all()
    form = SignupForm()

    return render(request, 'signup.html', {'form': form, 'classes': classes, 'error': error, })


def logout_user(request):
    if request.user.is_authenticated():
        logout(request)
        return HttpResponseRedirect('/login')
