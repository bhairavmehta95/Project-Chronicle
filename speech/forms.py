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
    password = forms.CharField(label='Password', max_length=20, widget=forms.PasswordInput())
    retyped = forms.CharField(label='Retype Password', max_length=20,widget=forms.PasswordInput())

class TeacherSignupForm(forms.Form):
    username = forms.CharField(label='Username', max_length=20)
    email = forms.EmailField(label='Email', max_length=30)
    #class_name = forms.CharField(label = 'Class', max_length = 20)
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
    is_qbuilder_update = forms.BooleanField(label='', initial=True, widget=forms.HiddenInput())

    def empty_init(self, *args, **kwargs):
        primary_keywords = kwargs.pop('primary_keywords', 0)
        secondary_keywords = kwargs.pop('secondary_keywords', 0)
        data = kwargs.pop('data')
    
        super(QBuilderUpdateForm, self).__init__(*args, **kwargs)
        
        self.fields['question_title'] = forms.CharField(label='Question Title', max_length=75, initial=data['question_title'])
        self.fields['num_primary_keywords'] = forms.IntegerField(label='', initial=primary_keywords, widget=forms.HiddenInput())
        self.fields['num_secondary_keywords'] = forms.IntegerField(label='', initial=secondary_keywords, widget=forms.HiddenInput())
        self.fields['raw_text'] = forms.CharField(label='', initial=data['raw_text'], widget=forms.HiddenInput)

        for index in range(primary_keywords):
            # generate extra fields in the number specified via extra_fields
            self.fields['primary_keyword_field_{index}'.format(index=index)] = forms.CharField(\
                                                                                                                        initial=data['primary_keyword_field_{index}'.format(index=index)]
                                                                                                                        )
           
            self.fields['primary_keyword_point_field_{index}'.format(index=index)] = forms.IntegerField(
                                                                                                                                initial=data['primary_keyword_point_field_{index}'.format(index=index)],
                                                                                                                                min_value=1
                                                                                                                                )
            
        for index in range(secondary_keywords):
            self.fields['secondary_keyword_field_{index}'.format(index=index)] = forms.CharField(
                                                                                                                        label='', 
                                                                                                                        initial=data['secondary_keyword_field_{index}'.format(index=index)],
                                                                                                                        widget=forms.HiddenInput()
                                                                                                                        ) 
            self.fields['secondary_keyword_point_field_{index}'.format(index=index)] = forms.IntegerField(
                                                                                                                        label='', 
                                                                                                                        initial=data['secondary_keyword_point_field_{index}'.format(index=index)],
                                                                                                                        widget=forms.HiddenInput()
                                                                                                                        ) 

        return self

class IntegerValidatorForm(forms.Form):
    integer = forms.IntegerField()

class StringValidatorForm(forms.Form):
    string = forms.CharField() 