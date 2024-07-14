from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .models import Email
from contacts.models import Invoice
from django.conf import settings

def send_invoice_email(request, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    contact = invoice.contact
    subject = f'Invoice #{invoice.id} - Due Payment'
    body = f"Dear {contact.name},\n\nHere are the details of your invoice:\n{invoice.details}"

    try:
        send_mail(subject, body, settings.EMAIL_HOST_USER, [contact.email])
        delivery_status = 'Sent'
    except:
        delivery_status = 'Failed'

    Email.objects.create(
        invoice=invoice,
        subject=subject,
        body=body,
        delivery_status=delivery_status,
        times_sent=1
    )
    return redirect('some-view')  # Replace with an appropriate redirect

def email_list(request):
    emails = Email.objects.all()
    return render(request, 'email/email_list.html', {'emails': emails})
