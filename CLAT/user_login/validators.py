from django import forms
import re

def validate_otp(value):
	rule = re.compile(r'(^[A-Z0-9]{6}$)')
	if not rule.search(value):
		raise forms.ValidationError('Please insert valid OTP code.')

