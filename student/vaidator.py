from django import forms
from teacher.validators import phone_regex

def user_exist(value):
	rule = re.compile(r'(^[+0-9]{1,3})*([0-9]{10,11}$)')
	if not rule.search(value):
		raise forms.ValidationError('Please add valid mobile number')