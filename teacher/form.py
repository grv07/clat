from django import forms
from user_login.form import MyForm
from django.contrib.auth.models import User
from teacher.validators import validate_password,phone_regex
from student.form import AddressForm
from student.models import Student
from .models import Teacher
from django.core.validators import MinLengthValidator, RegexValidator

class TeacherRegistrationForm(AddressForm):
    username = forms.CharField(max_length=20, label='username', validators=[MinLengthValidator(4),RegexValidator(r'^[a-zA-Z0-9_.-]+$', message='No spaces are allowed. Only _ . - special characters are allowed.')])
    full_name = forms.CharField(max_length=30, label='Full name', validators=[MinLengthValidator(4)])
    email = forms.EmailField(max_length=70, label='email_id')
    password = forms.CharField(max_length=20, label='password', validators=[validate_password, MinLengthValidator(4)])
    phone_number = forms.CharField(validators=[phone_regex, MinLengthValidator(10)],max_length=10,label='phone number')
    higher_education = forms.CharField(max_length = 100, label='higher education')
    gender = forms.CharField(max_length = 6, label='gender')
    d_o_b = forms.DateField(widget=forms.TextInput(), label='date of birth')
    i_agree = forms.BooleanField(label="check on Clat terms and services")


    def clean_username(self):
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).count() > 0:
            raise forms.ValidationError("We have a user with this user name")
        return data

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).count() > 0:
            raise forms.ValidationError("We have a user with this email-id")
        return data
        
    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']
        if Student.objects.filter(phone_number=data).count()>0 or Teacher.objects.filter(phone_number=data).count()>0:
            raise forms.ValidationError("We have a user with this phone number")
        return data