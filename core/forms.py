from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from core.models import Restaurant, Meal,Vehicle,Courier


class SignUpForm(UserCreationForm):
  email = forms.EmailField(max_length=250)
  first_name = forms.CharField(max_length=150)
  last_name = forms.CharField(max_length=150)
  phone_number = forms.CharField(max_length=11)
  company = forms.CharField(max_length=150)


  class Meta:
    model = User
    fields = ('email','first_name', 'last_name', 'password1', 'password2', 'phone_number','company')

  def clean_email(self):
    email = self.cleaned_data['email'].lower()
    if User.objects.filter(email=email):
      raise ValidationError("This email address already exists.")
    return email

class UserForm(forms.ModelForm):
  email = forms.CharField(max_length=100, required=True)
  password = forms.CharField(widget=forms.PasswordInput())
  
  class Meta:
    model = User
    fields = ("username", "password", "first_name", "last_name", "email")

class RestaurantForm(forms.ModelForm):
  class Meta:
    model = Restaurant
    fields = ("name", "phone", "address")

class AccountForm(forms.ModelForm):
  email = forms.CharField(max_length=100, required=True)

  class Meta:
    model = User
    fields = ("first_name", "last_name", "email")

class MealForm(forms.ModelForm):
  class Meta:
    model = Meal
    exclude = ("restaurant",)
    
from core.models import Courier

class PayoutForm(forms.ModelForm):
  class Meta:
    model = Courier
    fields = ('paypal_email',)
    
    


class BasicInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class VehicleInfoForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['year', 'make', 'model', 'color']

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Courier
        fields = ['resume', 'license', 'registration', 'insurance']
