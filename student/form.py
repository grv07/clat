from django import forms
from user_login.form import MyForm
from django.contrib.auth.models import User
from teacher.validators import validate_password,phone_regex
from .models import Student, ProfilePicture
from teacher.models import Teacher
from django.core.validators import MinLengthValidator,RegexValidator



class UserForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class AddressForm(MyForm):
    country = forms.CharField(label='country')
    street1 = forms.CharField(label='street 1', required=True)
    street2 = forms.CharField(label='street 2', required=False)
    pincode = forms.CharField(label='pincode', required=True)



class StudentRegistrationForm(AddressForm):
    username = forms.CharField(max_length=20, label='username', validators=[MinLengthValidator(4),RegexValidator(r'^[a-zA-Z0-9_.-]+$', message='No spaces are allowed. Only _ . - special characters are allowed.')])
    full_name = forms.CharField(max_length=30, label='full name', validators=[MinLengthValidator(4)])
    email = forms.EmailField(max_length=70, label='email')
    phone_number = forms.CharField(validators=[phone_regex, MinLengthValidator(10)],max_length=10,label='phone number')
    password = forms.CharField(max_length=20, label='password', validators=[validate_password, MinLengthValidator(4)])
    higher_education = forms.CharField(max_length = 100, label='higher education')
    gender = forms.CharField(max_length = 6, label='gender')
    i_agree = forms.BooleanField(label="check on Clat terms and services")
    d_o_b = forms.DateField(widget=forms.TextInput(), label='date of birth')

    def clean_username(self):
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).count() > 0:
            raise forms.ValidationError("We have a user with this user name")
        return data


    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).count() > 0:
            raise forms.ValidationError("We have a user with this user email-id")
        return data

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']
        if Student.objects.filter(phone_number=data).count()>0 or Teacher.objects.filter(phone_number=data).count()>0:
            raise forms.ValidationError("We have a user with this phone number")
        return data

class ProfilePictureForm(forms.ModelForm):
    picture=forms.ImageField(label='Profile Picture',required=False,error_messages ={'invalid':"Image files only"},\
                                   widget=forms.FileInput(attrs={'id':'uploaded_picture','style':'display: none;'}))
    
    class Meta:
        model = ProfilePicture
        fields = ('picture',)


class StudentProfileForm(AddressForm):
    full_name = forms.CharField(max_length=40, label='Full name')
    phone_number = forms.CharField(validators=[phone_regex],max_length=10,label='Phone number')
    gender = forms.CharField(max_length=10, label='Gender')
    d_o_b = forms.DateField(widget=forms.TextInput(), label='Date of Birth')
    higher_education = forms.CharField(max_length = 100, label='Higher Education')


    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(StudentProfileForm, self).__init__(*args, **kwargs)

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']
        if Student.objects.filter(phone_number=data).exclude(student=User.objects.get(id=self.request.user.id)).count()>0 or Teacher.objects.filter(phone_number=data).count()>0:
            raise forms.ValidationError("We have a user with this phone number")
        return data

    def clean_pincode(self):
        data = self.cleaned_data['pincode']
        import re
        if not re.match(r'^\d{6}$',data):
            raise forms.ValidationError("Pincode is not valid.")
        return data

    class Meta:
        model = Student
        fields = '__all__'
