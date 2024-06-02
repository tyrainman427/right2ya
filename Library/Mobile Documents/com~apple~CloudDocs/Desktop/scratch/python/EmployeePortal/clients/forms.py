from django import forms
from .models import *
from django.forms import ClearableFileInput

class DocumentForm(forms.ModelForm):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Document
        fields = ['docs']

# class UploadFileForm(forms.ModelForm):
#     class Meta:
#         upload = UploadFile
#         fields = '__all__'
