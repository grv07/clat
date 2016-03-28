from django.db import models
from django.forms import ModelForm
from user_login.models import Address
from teacher.validators import phone_regex
from django.contrib.auth.models import User
import uuid

class Teacher(User):
    uuid_key = models.TextField(max_length=100)
    full_name = models.TextField(max_length=100)
    address = models.OneToOneField(Address)
    phone_number = models.CharField(validators=[phone_regex],max_length = 15,unique=True)
    gender = models.CharField(max_length=50, null=True)
    d_o_b = models.DateField(null=True)
    higher_education = models.TextField(max_length = 100,null = True)
    added_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    i_agree = models.BooleanField(default=False)

    
    def __unicode__(self):
        print 'Teacher id: '
        return unicode(self.full_name)+"\t"+unicode(self.phone_number)


class TeacherModel(ModelForm):
    class Meta:
        model = Teacher
        fields = ['username', 'email', 'full_name','phone_number','i_agree','higher_education']

# Create your models here.
