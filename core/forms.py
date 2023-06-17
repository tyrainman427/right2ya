from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from core.models import Restaurant, Meal

class SignUpForm(UserCreationForm):
  email = forms.EmailField(max_length=250)
  first_name = forms.CharField(max_length=150)
  last_name = forms.CharField(max_length=150)
  phone_number = forms.CharField(max_length=11)
  company_name = forms.CharField(max_length=150)
  logo = forms.CharField(max_length=150)
  company_address = forms.CharField(max_length=150)
  logo = forms.ImageField(required=False)

  class Meta:
    model = User
    fields = ('email','company_name', 'first_name', 'last_name', 'password1', 'password2', 'phone_number','company_address', 'logo')
    
  def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            restaurant = Restaurant(user=user, name=self.cleaned_data['company_name'], logo=self.cleaned_data['logo'])
            # Set other restaurant attributes based on the form fields
            restaurant.save()
        return user

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
    fields = ("name", "phone", "address", "logo")

class AccountForm(forms.ModelForm):
  email = forms.CharField(max_length=100, required=True)

  class Meta:
    model = User
    fields = ("first_name", "last_name", "email")

class MealForm(forms.ModelForm):
  class Meta:
    model = Meal
    exclude = ("restaurant",)
    