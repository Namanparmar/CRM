from django import forms
from .models import Lead
from django.contrib.auth.forms import UserCreationForm,UsernameField
from django.contrib.auth import get_user_model

User = get_user_model()

class LeadModelForm(forms.ModelForm):
	class Meta:
		model = Lead
		fields = (
			'first_name',
			'last_name',
			'age',
			'agent'
		)
	  




class LeadForm(forms.Form):
	first_name = forms.CharField(max_length=100)
	last_name = forms.CharField(max_length=100)
	age = forms.IntegerField()
	agent = forms.CharField(max_length=100)
	#image = forms.ImageField()


class CustomUserCreationForm(UserCreationForm):
	class Meta:
		model = User
		fields = ("username",)
		field_classes = {'username': UsernameField}


