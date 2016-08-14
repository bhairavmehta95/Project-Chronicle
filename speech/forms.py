from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30)
    password = forms.CharField(label='Password', max_length=30)

class SignupForm(forms.Form):
	username = forms.CharField(label='Username', max_length=30)
	email = forms.EmailField(label='Email', max_length=30)
	first_name = forms.CharField(label='First Name', max_length=30)
	last_name = forms.CharField(label='Last Name', max_length=30)
	password = forms.CharField(label='Password', max_length=30, widget=forms.PasswordInput())
	retyped = forms.CharField(label='Retype Password', max_length=30,widget=forms.PasswordInput())