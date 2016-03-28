from django import forms
import re


def validate_file_extension(value,_type):
    import os
    filename = os.path.splitext(value.name)[1]  # [0] returns path+filename
    ext = filename.split('.')[1]
    valid_extensions = _type
    if ext != valid_extensions:
        return 1
    elif not re.match(r'[ a-zA-Z0-9\-\(\)\*]', str(value)):
        return 2


def validate_yut_url(value):
    if 'youtube.com' in value and '?v=' in value:
        return 0
    else:
        return 1


def validate_weekly_module_name(value):
    if not re.match(r'^[ a-z0-9_&-:]*$', str(value),re.I) or len(value.strip())<4:
        raise forms.ValidationError('Must be 4 characters long. Only word characters are allowed including : / , * - + ) ( & _')

