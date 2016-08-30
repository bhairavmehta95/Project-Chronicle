from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=20)
    password = forms.CharField(label='Password', max_length=20, widget=forms.PasswordInput())

class TeacherLoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=20)
    password = forms.CharField(label='Password', max_length=20, widget=forms.PasswordInput())

class SignupForm(forms.Form):
	username = forms.CharField(label='Username', max_length=20)
	email = forms.EmailField(label='Email', max_length=30)
	first_name = forms.CharField(label='First Name', max_length=20)
	last_name = forms.CharField(label='Last Name', max_length=20)
	#teacher_id = forms.CharField(label='Teacher ID', max_length=30)
	password = forms.CharField(label='Password', max_length=20, widget=forms.PasswordInput())
	retyped = forms.CharField(label='Retype Password', max_length=20,widget=forms.PasswordInput())

class TeacherSignupForm(forms.Form):
	username = forms.CharField(label='Username', max_length=20)
	email = forms.EmailField(label='Email', max_length=30)
	class_name = forms.CharField(label = 'Class', max_length = 20)
	first_name = forms.CharField(label='First Name', max_length=20)
	last_name = forms.CharField(label='Last Name', max_length=20)
	teacher_id = forms.CharField(label='Teacher ID', max_length=20)
	password = forms.CharField(label='Password', max_length=20, widget=forms.PasswordInput())
	retyped = forms.CharField(label='Retype Password', max_length=20,widget=forms.PasswordInput())