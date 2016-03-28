from django import forms
from teacher.validators import phone_regex
from user_login.validators import validate_otp
from student.models import Student
from .models import Contact, Query


class MyForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(MyForm, self).__init__(*args, **kwargs)
        for k, field in self.fields.items():
            if 'required' in field.error_messages:
                field.error_messages['required'] = 'Please enter '+str(field.label)
    

class OTPVerify_mob_Form(MyForm):
    user_phone = forms.CharField(validators = [phone_regex], max_length = 10, label = 'phone number')

    def clean_user_phone(self):
        data = self.cleaned_data['user_phone']
        if not  Student.objects.filter(phone_number = data).count() > 0:
            raise forms.ValidationError("This phone number not register with us !")
        return data

class OTPVerify_code_Form(MyForm):
    otp_code = forms.CharField(validators = [validate_otp], max_length = 6, label = 'OTP Code')

    def clean_otp_code(self):
        data = self.cleaned_data['otp_code']
        if not  Student.objects.filter(otp_code = data).count() > 0:
            raise forms.ValidationError("This OTP is not valid !")
        return data        



class ContactForm(forms.ModelForm):
    phone = forms.CharField(validators = [phone_regex], max_length = 10, label = 'phone number')
    iama = forms.CharField(max_length=27, label='profession')
    email = forms.EmailField()
    fullname = forms.CharField(max_length=30,label='full name')
    inquirytype = forms.CharField(max_length=60,label='inquiry type')
    message = forms.CharField(max_length=500,label='message')

    class Meta:
        model = Contact
        fields = ('phone', 'email', 'iama','fullname','inquirytype','message')

class ContactForm(forms.ModelForm):
    phone = forms.CharField(validators = [phone_regex], max_length = 10, label = 'phone number')
    iama = forms.CharField(max_length=27, label='profession')
    email = forms.EmailField()
    fullname = forms.CharField(max_length=30,label='full name')
    inquirytype = forms.CharField(max_length=60,label='inquiry type')
    message = forms.CharField(max_length=500,label='message')

    class Meta:
        model = Contact
        fields = ('phone', 'email', 'iama','fullname','inquirytype','message')   
        
class QueryForm(forms.ModelForm):
    course_id = forms.IntegerField()
    course_name = forms.CharField(max_length = 100)
    username = forms.CharField(max_length = 30)
    module_name = forms.CharField(max_length = 500)
    user_email = forms.EmailField()
    message = forms.CharField(max_length = 500)
    iama = forms.CharField(max_length=27, label='profession')

    class Meta:
        model = Query
        fields = '__all__'          


