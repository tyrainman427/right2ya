from django import forms

from django.contrib.auth.models import User
from django.db import models
from core.models import Customer, Service

class UserForm(forms.ModelForm):
  email = forms.CharField(max_length=100, required=True)
  password = forms.CharField(widget=forms.PasswordInput())
  
  class Meta:
    model = User
    fields = ("username", "password", "first_name", "last_name", "email")

# class RestaurantForm(forms.ModelForm):
#   class Meta:
#     model = Restaurant
#     fields = ("name", "phone", "address", "logo")

# class AccountForm(forms.ModelForm):
#   email = forms.CharField(max_length=100, required=True)

#   class Meta:
#     model = User
#     fields = ("first_name", "last_name", "email")

class ServiceForm(forms.ModelForm):
  class Meta:
    model = Service
    exclude = ("restaurant",)
