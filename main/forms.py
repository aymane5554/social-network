from .models import User
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm

class User_form(UserCreationForm):
	class Meta :
		model = User
		fields = ["username","password1","password2","image","bio"]

class Profile_form(ModelForm):
	class Meta :
		model = User
		fields = ["username","bio","image"]