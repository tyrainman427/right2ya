from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model
from twilio.rest import Client
from django.contrib.sites.shortcuts import get_current_site  
from django.template.loader import render_to_string  
from django.utils.encoding import force_bytes, force_text  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.http import HttpResponse  
from .token import account_activation_token  
from django.contrib.auth.models import User  
from django.core.mail import EmailMessage  
from rest_framework.views import APIView
from rest_framework import viewsets
from django.http import JsonResponse
from datetime import datetime, timedelta
from .models import Job
from .serializers import JobSerializer


from . import forms
from django.conf import settings


def home(request):
    return render(request, 'home.html')

# def sign_up(request):
#     form = forms.SignUpForm()

#     if request.method == 'POST':
#         form = forms.SignUpForm(request.POST)

#         if form.is_valid():
#             email = form.cleaned_data.get('email').lower()

#             user = form.save(commit=False)
#             user.username = email
#             user.is_active = False
#             user.save()

#             login(request, user, backend='django.contrib.auth.backends.ModelBackend')
#             return redirect('/')

#     return render(request, 'sign_up.html', {
#         'form': form
#     })

def sign_up(request):  
    if request.method == 'POST':  
        form = forms.SignUpForm(request.POST)  
        
        if form.is_valid():  
            email = form.cleaned_data.get('email').lower()
            # save form in the memory not in database  
            user = form.save(commit=False)  
            user.username = email
            user.is_active = False  
            user.save()  
            # to get the domain of the current site  
            current_site = get_current_site(request)  
            mail_subject = 'Welcome to Right 2 Ya Beta!'  
            message = render_to_string('acc_active_email.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            })  
            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
            email.send()  
            return HttpResponse('Please confirm your email address to complete the registration')  
    else:  
        form = forms.SignUpForm()  
    return render(request, 'sign_up.html', {'form': form})  

def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_text(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return HttpResponse(f"Thank you for your email confirmation. Now you can login your account.")  
    else:  
        return HttpResponse('Activation link is invalid!') 
    
from rest_framework import generics

class AvailableJobsAPIView(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    
 

class AvailableJobsView(APIView):
    def get(self, request):
        pickup_datetime = datetime.now()
        delivery_datetime = pickup_datetime + timedelta(hours=2)
        available_jobs = Job.objects.filter(status=Job.PROCESSING_STATUS)
        # data = [{"id": job.id, "pickup_address": job.pickup_address, "delivery_address": job.delivery_address} for job in available_jobs]
       
        return JsonResponse({"available_jobs": available_jobs})