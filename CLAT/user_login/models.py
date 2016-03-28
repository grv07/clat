from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from admin_resumable.fields import ModelAdminResumableFileField
from django import forms

class City(models.Model):
    city_name = models.CharField(max_length = 100,unique = True)
    city_state = models.CharField(max_length = 100)

    class Meta:
        ordering = ['city_name']
    



"""
Address model for storing address
"""
class Address(models.Model):
    city_obj = models.ForeignKey(City, unique=False)
    country = models.CharField(max_length=200)
    street1 = models.TextField(max_length=100)
    street2 = models.TextField(max_length=100,blank=True)
    pincode = models.TextField(max_length=6)
    added_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


class AddressModel(ModelForm):

    def clean_pincode(self):
        data = self.cleaned_data['pincode']
        import re
        if not re.match(r'^\d{6}$', data):
            raise forms.ValidationError("Pincode is not valid.")
        return data
    class Meta:
        model = Address
        fields = ['country', 'street1', 'street2', 'pincode']


class Foo(models.Model):
    bar = models.CharField(max_length=200)
    foo = ModelAdminResumableFileField()


"""
Contact modal for storing contact info
"""
class Contact(models.Model):
    phone = models.CharField(max_length=10)
    iama = models.CharField(max_length=27)
    email = models.EmailField()
    fullname = models.CharField(max_length=30)
    inquirytype = models.CharField(max_length=60)
    message = models.CharField(max_length=500)

    added_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


"""
Query modal for storing query info about a course ...
"""
class Query(models.Model):
    course_id = models.IntegerField()
    course_name = forms.CharField(max_length = 100)
    username = models.CharField(max_length = 30)
    module_name = models.CharField(max_length = 500)
    user_email = models.EmailField()
    message = models.CharField(max_length = 500)
    iama = models.CharField(max_length=27)

    added_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

# Create your models here.
