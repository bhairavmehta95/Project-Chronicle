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

class QuestionBuilderForm(forms.Form):
    question_title = forms.CharField(label='Question Title', max_length=75)
    sources = forms.CharField(label='Source', widget=forms.Textarea)
    keywords_to_return = forms.IntegerField(label='Keywords to Return', min_value=1, max_value=30)

class QBuilderUpdateForm(forms.Form):
    question_title = forms.CharField(label='Question Title', max_length=75)

    def __init__(self, *args, **kwargs):
        keywords = kwargs.pop('keywords', 0)
    
        super(QBuilderUpdateForm, self).__init__(*args, **kwargs)

        for index in range(int(keywords)):
            # generate extra fields in the number specified via extra_fields
            self.fields['keyword_field_{index}'.format(index=index)] = forms.CharField()
            self.fields['keyword_point_field_{index}'.format(index=index)] = forms.IntegerField(min_value=1)
