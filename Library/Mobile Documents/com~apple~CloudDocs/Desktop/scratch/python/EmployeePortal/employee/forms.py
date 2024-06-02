from django import forms
from .models import *
import datetime
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm, DateInput


class EventForm(ModelForm):
  class Meta:
    model = Event
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
      'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
    }
    fields = '__all__'

  def __init__(self, *args, **kwargs):
    super(EventForm, self).__init__(*args, **kwargs)
    # input_formats to parse HTML5 datetime-local input to datetime field
    self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)

class AnnouncementForm(forms.ModelForm):
    title = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Announcement
        fields = ('title','message')

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)
