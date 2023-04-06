from django.shortcuts import render, redirect
from django.contrib.auth import login
from twilio.rest import Client
from .serializers import JobSerializer
from rest_framework import viewsets, permissions, serializers
from rest_framework.response import Response
from .models import Job
from . import forms
from django.conf import settings



def home(request):
    return render(request, 'home.html')

def sign_up(request):
    form = forms.SignUpForm()

    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email').lower()

            user = form.save(commit=False)
            user.username = email
            user.save()

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/')

    return render(request, 'sign_up.html', {
        'form': form
    })
    
class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    queryset = Job.objects.all()
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        job = serializer.save()
        return Response(JobSerializer(job).data)
