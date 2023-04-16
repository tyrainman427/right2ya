from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db import models
from .models import Job
from twilio.rest import Client
import os
from django.urls import reverse
from allauth.account.signals import user_signed_up
from allauth.account.utils import send_email_confirmation

@receiver(user_signed_up)
def send_email_verification(sender, request, user, **kwargs):
    send_email_confirmation(request, user)


 
# @receiver(post_save, sender=User)
# def send_welcome_email(sender, instance, created, **kwargs):
#     if created and instance.email:
#         body = render_to_string(
#             'welcome_email_template.html',
#             {
#                 'name': instance.get_full_name
#             }
#         )
#         # send welcome email
#         send_mail(
#             'Welcome to Right 2 Ya Beta',
#             body,
#             settings.DEFAULT_FROM_EMAIL,
#             [instance.email],
#             fail_silently=False,
        # )
@receiver(post_save, sender=Job)
def send_update_email(sender, instance, **kwargs):   
    if instance.status != instance.CREATING_STATUS:
        #print('Sending update email')
        TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
        TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        message = client.messages.create(
                                body=f'Your order has been updated and its status has changed to {instance.status}. If you need further information please check the app.',
                                from_='+18446702408',
                                to='+12037150447' 
                            )
 
        subject = f'Job status changed to {instance.status}'
        body = f'Your order {instance.name} has been updated and its status has changed to {instance.status}.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = ['info@worknscrubs.com']
        send_mail(subject, body, from_email, recipient_list)