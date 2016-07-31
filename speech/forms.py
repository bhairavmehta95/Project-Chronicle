from django import forms

class SignupForm(forms.Form):
    f_name = forms.CharField(label='First Name', max_length=30)
    l_name = forms.CharField(label='Last Name', max_length=30)
    