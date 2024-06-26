from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from core.models import Meal, Restaurant

class SignUpForm(UserCreationForm):
  email = forms.EmailField(max_length=250)
  first_name = forms.CharField(max_length=150)
  last_name = forms.CharField(max_length=150)
  phone_number = forms.CharField(max_length=15, required=False)


  class Meta:
    model = User
    fields = ('email', 'first_name', 'last_name', 'password1', 'password2','phone_number')

  def clean_email(self):
    email = self.cleaned_data['email'].lower()
    if User.objects.filter(email=email):
      raise ValidationError("This email address already exists.")
    return email

class UserForm(forms.ModelForm):
  email = forms.CharField(max_length=100, required=True)
  phone_number = forms.CharField(max_length=15, required=False)

  password = forms.CharField(widget=forms.PasswordInput())
  
  class Meta:
    model = User
    fields = ("username", "password", "first_name", "last_name", "email","phone_number")

class RestaurantForm(forms.ModelForm):
  class Meta:
    model = Restaurant
    fields = ("name", "address")
    
    labels ={
      'name':'Company Name',
    }

class AccountForm(forms.ModelForm):
  email = forms.CharField(max_length=100, required=True)

  class Meta:
    model = User
    fields = ("first_name", "last_name", "email")

class MealForm(forms.ModelForm):
  class Meta:
    model = Meal
    exclude = ("restaurant",)
