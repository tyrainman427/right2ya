from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db import models
from .models import Job, Notification
from twilio.rest import Client
import os
from django.urls import reverse
from allauth.account.signals import user_signed_up
from allauth.account.utils import send_email_confirmation

@receiver(user_signed_up)
def send_email_verification(sender, request, user, **kwargs):
    send_email_confirmation(request, user)


@receiver(post_save, sender=Job)
def create_or_update_notification(sender, instance, created, **kwargs):
    if instance.status == instance.PROCESSING_STATUS:
        # Create a notification when a job is created, only if it doesn't exist already
        notification, created = Notification.objects.get_or_create(user=instance.customer.user, job=instance)
        if created:
            print("Job notification created")
    elif instance.status == instance.READY_STATUS:
        # Update the notification to read=True when job status is READY_STATUS
        Notification.objects.filter(user=instance.customer.user, job=instance).update(read=True)
        print("Job notification updated")


@receiver(post_save, sender=Job)
def send_receipt_email(sender, instance, **kwargs):
 
    if instance.paid_status == 'paid': 
        print(instance.customer.user.email)# replace with the actual status for 'Paid'
        subject = f'Receipt for job {instance.name}'
        body = f'Thank you for your payment. This email is a receipt for your job {instance.name}.\n\n' \
               f'Description: {instance.description}\n' \
               f'Price: ${instance.price}\n'  # replace with the actual field for the job's price
        from_email = settings.DEFAULT_FROM_EMAIL  # replace with your email
        recipient_list = [instance.customer.user.email]  # replace with the customer's email field

        send_mail(subject, body, from_email, recipient_list)


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
        recipient_list = [instance.customer.user.email]
        send_mail(subject, body, from_email, recipient_list)