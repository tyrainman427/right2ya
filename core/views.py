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
from .models import *
from .serializers import JobSerializer
from django.urls import reverse
from django.shortcuts import get_object_or_404
from . import forms
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes



def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "registration/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Right2ya Beta',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'Right2ya Beta' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="registration/password_reset.html", context={"password_reset_form":password_reset_form})

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
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            activation_url = reverse('activate', kwargs={
                'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            full_activation_url = request.build_absolute_uri(activation_url)
            print('Activation URL:', full_activation_url)
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = forms.SignUpForm()
    return render(request, 'sign_up.html', {'form': form})

    # if request.method == 'POST':  
    #     form = forms.SignUpForm(request.POST)  
        
    #     if form.is_valid():  
    #         email = form.cleaned_data.get('email').lower()
    #         # save form in the memory not in database  
    #         user = form.save(commit=False)  
    #         user.username = email
    #         user.is_active = False  
    #         user.save()  
    #         # to get the domain of the current site  
    #         current_site = get_current_site(request)  
    #         mail_subject = 'Welcome to Right 2 Ya Beta!'  
    #         message = render_to_string('acc_active_email.html', {  
    #             'user': user,  
    #             'domain': current_site.domain,  
    #             'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
    #             'token':account_activation_token.make_token(user),  
    #         })  
    #         to_email = form.cleaned_data.get('email')  
    #         email = EmailMessage(  
    #                     mail_subject, message, to=[to_email]  
    #         )  
    #         email.send()  
    #         return HttpResponse('Please confirm your email address to complete the registration')  
    # else:  
    #     form = forms.SignUpForm()  
    # return render(request, 'sign_up.html', {'form': form})  

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
    

# def rate_courier(request, courier_id):
#     if request.method == 'POST':
#         rating_value = request.POST.get('rating')
#         print("Rating:", type(rating_value))
#         if rating_value is not None:
#             review_text = request.POST.get('comment')
            
#             # Fetch the Courier instance from the database
#             courier = Courier.objects.get(id=courier_id)

#             rating = Rating(courier=courier, rating_value=rating_value, review_text=review_text)
#             rating.save()
    
#     return render(request, 'customer/rate_courier.html')

def rate_courier(request, job_id):
    if request.method == 'POST':
        rating_value = request.POST.get('rating')
        review_text = request.POST.get('comment')
        
        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            # Handle the case when the job does not exist
            pass
        else:
            if not job.rated and job.courier:
                # Create a new Rating instance and save it
                rating = Rating(courier=job.courier, rating_value=rating_value, review_text=review_text)
                rating.save()
                job.rated = True
                job.status = Job.REVIEWED_STATUS
                job.save()
    
    return render(request, 'customer/jobs.html')


