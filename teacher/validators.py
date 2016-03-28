from django import forms
import re


def validate_password(value):
    pattern = "^(?=.*?[a-zA-Z])(?=.*?[0-9])(?=.*?[@#&^%!*%$])[a-zA-Z0-9@#&^%!*%$]{8,20}$"

    if not re.findall(pattern, str(value)):
        raise forms.ValidationError(
            "Password must contains a uppercase letters: A-Z,lowercase letters: a-z,numbers: 0-9 and any of the special characters: @#$%^&+=")
    return value

def phone_regex(value):
	pattern = r'^([789]\d{9})$'
	rule = re.compile(pattern)
	if not rule.search(value):
		raise forms.ValidationError('Mobile number must be in Indian format.')

