from django import forms
from .models import ScheduledJob
from core.models import Job

class ScheduledJobForm(forms.ModelForm):
    class Meta:
        model = ScheduledJob
        fields = ['pickup_address', 'delivery_address', 'scheduled_datetime']

    # Add any additional form fields or customization as needed
class DateInput(forms.DateInput):
    input_type = 'date'
        
class TimeInput(forms.TimeInput):
      input_type = 'time'
      format = '%H:%M:%S'

class JobCreateStep1Form(forms.ModelForm):
  class Meta:
    model = ScheduledJob
    fields = ('name', 'description', 'category','quantity', 'photo','delivery_date_time','delivery_time')
    widgets = {
            'delivery_date_time': DateInput(),
            'delivery_time': TimeInput(),
        }
    
class JobCreateStep2Form(forms.ModelForm):
  pickup_address = forms.CharField(required=True)
  pickup_name = forms.CharField(required=True)
  pickup_phone = forms.CharField(required=True)

  class Meta:
    model = ScheduledJob
    fields = ('pickup_address', 'pickup_lat', 'pickup_lng', 'pickup_name', 'pickup_phone')

class JobCreateStep3Form(forms.ModelForm):
  delivery_address = forms.CharField(required=True)
  delivery_name = forms.CharField(required=True)
  delivery_phone = forms.CharField(required=True)

  class Meta:
    model = ScheduledJob
    fields = ('delivery_address', 'delivery_lat', 'delivery_lng', 'delivery_name', 'delivery_phone')