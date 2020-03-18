from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


"""
Fields based on the following:
https://webarchive.nationalarchives.gov.uk/+/http://www.cabinetoffice.gov.uk/media/254290/GDS%20Catalogue%20Vol%202.pdf
"""


class UserRegisterForm(UserCreationForm):
	email = forms.EmailField(max_length=150)
	first_name = forms.CharField(max_length=35, label='Imię')
	last_name = forms.CharField(max_length=35, label='Nazwisko')

	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField(max_length=150)
	first_name = forms.CharField(max_length=35, label='Imię')
	last_name = forms.CharField(max_length=35, label='Nazwisko')

	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email']



class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['image']