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

@receiver(pre_save, sender=Job)
def set_previous_status(sender, instance, **kwargs):
    try:
        obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        # Object is new, so field hasn't technically changed, but you may want to do something else here.
        pass
    else:
        instance.previous_status = obj.paid_status  # Store the previous value


@receiver(post_save, sender=Job)
def handle_job_update(sender, instance, **kwargs):
    # For receipt email
    if instance.status == instance.COMPLETED_STATUS:
        send_receipt_email(instance)

    # For status update email
    if instance.status != instance.CREATING_STATUS and instance.status != instance.previous_status:
        send_status_update_email(instance)

@receiver(pre_save, sender=Job)
def store_previous_status(sender, instance, **kwargs):
    try:
        obj = sender.objects.get(pk=instance.pk)
        instance.previous_status = obj.status
    except sender.DoesNotExist:
        pass

def send_receipt_email(instance):
    subject = f'Receipt for job {instance.name}'
    body = f'Thank you for your payment. This email is a receipt for your job {instance.name}.\n\n' \
           f'Description: {instance.description}\n' \
           f'Price: ${instance.price}\n'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [instance.customer.user.email]
    send_mail(subject, body, from_email, recipient_list)

def send_status_update_email(instance):
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    message = client.messages.create(
        body=f'Your order has been updated and its status has changed to {instance.status}. If you need further information please check the app.',
        from_='+18446702408',
        to=[instance.customer.phone_number]
    )

    subject = f'Job status changed to {instance.status}'
    body = f'Your order {instance.name} has been updated and its status has changed to {instance.status}.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [instance.customer.user.email]
    send_mail(subject, body, from_email, recipient_list)
