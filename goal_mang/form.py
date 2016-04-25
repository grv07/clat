from django import forms

from models import Goal

class CreateGoalForm(forms.ModelForm):
	enr_course = forms.CharField()
	# user = forms.CharField()

	class Meta:
		model = Goal
		exclude = ['enr_course', 'user', 'added_date', 'updated_date']