from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User

from core.models import *

class BasicUserForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ('first_name', 'last_name')

class BasicCustomerForm(forms.ModelForm):
  class Meta:
    model = Customer
    fields = ('avatar',)
    
class DateInput(forms.DateInput):
    input_type = 'date'
        
class TimeInput(forms.TimeInput):
      input_type = 'time'
      format = '%H:%M:%S'

class JobCreateStep1Form(forms.ModelForm):
  class Meta:
    model = Job
    fields = ('name', 'description', 'category', 'size', 'quantity', 'photo','weight', 'has_spill','service_type','scheduled_date')
    widgets = {
            'scheduled_date': DateInput(),
            'scheduled_time': TimeInput(),
        }
    labels = {
            'name': 'Item Name',
        }

class JobCreateStep2Form(forms.ModelForm):
  pickup_address = forms.CharField(required=True)
  pickup_name = forms.CharField(required=True)
  pickup_phone = forms.CharField(required=True)

  class Meta:
    model = Job
    fields = ('pickup_address', 'pickup_lat', 'pickup_lng', 'pickup_name', 'pickup_phone')

class JobCreateStep3Form(forms.ModelForm):
  delivery_address = forms.CharField(required=True)
  delivery_name = forms.CharField(required=True)
  delivery_phone = forms.CharField(required=True)

  class Meta:
    model = Job
    fields = ('delivery_address', 'delivery_lat', 'delivery_lng', 'delivery_name', 'delivery_phone')
    

class AddTipForm(forms.Form):
    tip = forms.DecimalField(max_digits=6, decimal_places=2)
