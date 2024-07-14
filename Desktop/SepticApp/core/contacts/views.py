from django.http import HttpResponse, JsonResponse  
from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth import login, authenticate, logout  
from .forms import SignupForm, AppointmentForm  
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from contacts.token import account_activation_token  
from django.contrib.auth.models import User  
from django.core.mail import EmailMessage , send_mail
from django.conf import settings
from django.urls import reverse
import json
from django.contrib.auth import get_user_model
from .forms import ContactForm, PropertyForm, PaymentForm, InvoiceForm, PropertyImageForm, ServiceContractForm, DocumentFormSet
from django.contrib.auth.forms import AuthenticationForm
from .models import Property, Contact, Appointment, Invoice, PropertyImage, Document, Service
from workOrder.models import WorkOrder
from email_app.models import Email
from .models import Contact
from django.contrib.auth.decorators import login_required
import stripe
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.http import require_POST
from decimal import Decimal


google_api_key = settings.GOOGLE_API_KEY
stripe.api_key = settings.STRIPE_SECRET_KEY


#### Home Page ######
@login_required
def home(request):
    jobs_waiting = WorkOrder.objects.all()  # Adjust the query as per your requirement
    # Add other context data if needed
    return render(request, 'contacts/index.html', {'jobs_waiting': jobs_waiting})
  
def signup(request):  
    if request.method == 'POST':  
        form = SignupForm(request.POST)  
        if form.is_valid():  
            # save form in the memory not in database  
            user = form.save(commit=False)  
            user.is_active = False  
            user.save()  
            # to get the domain of the current site  
            current_site = get_current_site(request)  
            mail_subject = 'Activation link has been sent to your email id'  
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
        form = SignupForm()  
    return render(request, 'signup.html', {'form': form})  

def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')  
    else:  
        return HttpResponse('Activation link is invalid!')  

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Change 'home' to your desired redirect URL
            else:
                return HttpResponse('Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')  # Change 'login' to your desired redirect URL

   
#####################

def send_contact_email(request, contact_id):
    contact = Contact.objects.get(id=contact_id)

    # Define your email contents
    subject = "Email Subject Here"
    message = "Email message here"
    from_email = "your-email@example.com"
    recipient_list = [contact.email]

    # Send the email
    send_mail(subject, message, from_email, recipient_list)

    # Create an Email object for record-keeping
    Email.objects.create(
        contact=contact,
        subject=subject,
        body=message,
        # ... other fields as necessary ...
    )

    return JsonResponse({'status': 'Email sent successfully'})

@login_required
def property_list(request):
    properties = Property.objects.all()
 
    context = {
        'properties': properties,

    }
    return render(request, 'contacts/property_list.html', context)

@login_required
def property_detail(request, property_id):
    property = get_object_or_404(Property, pk=property_id)
    contact_id = property.contact.id 
    appointments = property.appointments.all() 
    return render(request, 'contacts/property_list.html', {'property': property, 'appointments': appointments,'contact_id': contact_id})

@login_required
def property_create(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)
    if request.method == "POST":
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property = form.save(commit=False)
            property.contact = contact  # Attach the contact to the property
            property.save()
            return redirect('contact_detail', contact_id=contact.id)  # Redirect to contact detail view
    else:
        form = PropertyForm()
        
        context = {
        'form': form,
        'google_api_key': settings.GOOGLE_API_KEY,
        'contact': contact
    }
    return render(request, 'contacts/property_form.html', context)

@login_required
def property_edit(request, property_id):
    property = get_object_or_404(Property, pk=property_id)
    if request.method == "POST":
        form = PropertyForm(request.POST, request.FILES, instance=property)
        if form.is_valid():
            form.save()
            return redirect('property_detail', property_id=property.id)  # Adjust this to the appropriate view
    else:
        form = PropertyForm(instance=property)
    return render(request, 'contacts/property_form.html', {'form': form})

@login_required
def contact_list(request):
    contacts = Contact.objects.all()
    return render(request, 'contacts/contact_list.html', {'contacts': contacts})

@login_required
def contact_detail(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)
    properties = contact.properties.all()
    all_invoices = Invoice.objects.filter(contact=contact)

    # Get all invoice IDs related to the contact
    invoice_ids = all_invoices.values_list('id', flat=True)

    # Fetch emails linked to these invoices
    emails = Email.objects.filter(invoice__id__in=invoice_ids)
    
    all_appointments = []
    for property in properties:
        appointments = property.appointments.all()
        all_appointments.extend(appointments)

    return render(request, 'contacts/contact_detail.html', {
        'contact': contact, 
        'properties': properties,
        'all_appointments': all_appointments,
        'all_invoices': all_invoices,
        'emails': emails
    })

@login_required
def contact_add(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact_list')
    else:
        form = ContactForm()
    return render(request, 'contacts/create_contact.html', {'form': form})

@login_required
def contact_edit(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)
    if request.method == "POST":
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('contact_detail', contact_id=contact.id)
    else:
        form = ContactForm(instance=contact)
        
    context = {
        'form': form,
        'google_api_key': settings.GOOGLE_API_KEY
    }

    return render(request, 'contacts/create_contact.html', context)
 
@login_required
def create_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            return redirect(reverse('contact_detail', args=[contact.id]))
    else:
        form = ContactForm()

    context = {
        'form': form,
        'google_api_key': settings.GOOGLE_API_KEY
    }

    return render(request, 'contacts/create_contact.html', context)

@login_required    
def create_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('property_list')  # Redirect to the property list page
    else:
        form = PropertyForm()
    return render(request, 'properties/create_property.html', {'form': form})

@login_required
@xframe_options_exempt
def create_payment_intent(request):
    intent = stripe.PaymentIntent.create(
        amount=1000,  # Amount in cents
        currency='usd',
        payment_method_types=['card'],
    )
    return render(request, 'contacts/create_payment_intent.html', {
        'client_secret': intent.client_secret,
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
    })

@login_required
def contact_list(request):
    sort = request.GET.get('sort', 'name')  # Default sorting by 'name'
    if sort == 'email':
        contacts = Contact.objects.all().order_by('email')
    else:
        contacts = Contact.objects.all().order_by('name')
    return render(request, 'contacts/contact_list.html', {'contacts': contacts})

@login_required
def property_documents(request, property_id):
    property = get_object_or_404(Property, pk=property_id)
    if request.method == 'POST':
        formset = DocumentFormSet(request.POST, request.FILES, queryset=Document.objects.none())
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    document = form.save(commit=False)
                    document.property = property
                    document.save()
            return redirect('property_documents', property_id=property.id)
    else:
        formset = DocumentFormSet(queryset=Document.objects.none())

    existing_documents = property.documents.all()

    return render(request, 'contacts/property_documents.html', {
        'formset': formset,
        'property': property,
     
        'existing_documents': existing_documents
    })

@login_required
def property_photos(request, property_id):
    property = get_object_or_404(Property, pk=property_id)
    photos = PropertyImage.objects.filter(property=property)
    return render(request, 'contacts/property_photos.html', {'property': property, 'photos': photos})

@login_required
def add_property_image(request, property_id):
    property = get_object_or_404(Property, pk=property_id)
    contact_id = property.contact.id
    if request.method == 'POST':
        form = PropertyImageForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            property_image = form.save(commit=False)
            property_image.property = property
            property_image.save()
            return redirect('contact_detail', contact_id=contact_id)

    else:
        form = PropertyImageForm()
    
    return render(request, 'contacts/add_property_image.html', {'form': form, 'property': property, 'contact_id': contact_id})

@login_required
def property_finances(request, property_id):
    property = get_object_or_404(Property, pk=property_id)
    # Assuming you have a finance-related field or method in your Property model
    finances = property.finances.all()
    return render(request, 'properties/property_finances.html', {'property': property, 'finances': finances})

@login_required
def create_appointment(request, property_id):
    property = get_object_or_404(Property, pk=property_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.property = property
            appointment.user = request.user 
            appointment.save()
            return redirect('appointment_detail', appointment_id=appointment.id)
    else:
        form = AppointmentForm()
    return render(request, 'create_appointment.html', {'form': form, 'property': property})

@login_required
def update_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointment_detail', appointment_id=appointment.id)
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'appointments/update_appointment.html', {'form': form, 'appointment': appointment})

@login_required
def appointment_detail(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    return render(request, 'contacts/appointment_detail.html', {'appointment': appointment})

@login_required
def create_invoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)  # Create but don't save the invoice yet
            
            # Generate the invoice number
            last_invoice = Invoice.objects.all().order_by('id').last()
            if last_invoice and last_invoice.invoice_number and last_invoice.invoice_number.isdigit():
                invoice.invoice_number = str(int(last_invoice.invoice_number) + 1)
            else:
                invoice.invoice_number = '1000'

            # Save the invoice initially to generate an ID
            invoice.save()
            form.save_m2m()


            # Now that the invoice has an ID, you can add services and calculate totals
            services = form.cleaned_data['services']
            subtotal = sum(service.price for service in services)
            service_fee = subtotal * Decimal('0.15')
            total = subtotal + service_fee

            # Set the calculated total and save the invoice again
            invoice.total = total
            invoice.save()


            return redirect('invoice_detail', invoice_id=invoice.id)
    else:
        form = InvoiceForm()
    return render(request, 'contacts/create_invoice.html', {'form': form})





@login_required
def invoice_detail(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    property = invoice.property  # Access the related property
    
    # Calculate the subtotal and service fee
    subtotal = sum(service.price for service in invoice.services.all())
    service_fee = subtotal * Decimal('0.15')
    
    return render(request, 'contacts/invoice_detail.html', {
        'invoice': invoice,
        'property': property,
        'subtotal': subtotal,
        'service_fee': service_fee,
    })
@login_required
def invoice_list(request):
    if request.method == 'POST':
        selected_invoices = request.POST.getlist('selected_invoices')
        # Logic to send emails for the selected invoices
        # ...
        return redirect('invoice_list')

    invoices = Invoice.objects.all()
    return render(request, 'contacts/invoice_list.html', {'invoices': invoices})

@login_required
def send_invoice_emails(request):
    if request.method == 'POST' and request.is_ajax():
        selected_invoice_ids = request.POST.getlist('selected_invoices')
        invoices = Invoice.objects.filter(id__in=selected_invoice_ids)

        for invoice in invoices:
            subject = f'Invoice {invoice.invoice_number}'
            message = f'Dear {invoice.contact.name},\n\nHere are the details of your invoice:\n...'
            # Add more details to the message as needed
            recipient_list = [invoice.contact.email]
            send_mail(subject, message, 'your-email@example.com', recipient_list)

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def email_invoice(request):
    if request.method == 'POST' and request.is_ajax():
        data = json.loads(request.body)
        invoice_id = data.get('invoice_id')
        invoice = Invoice.objects.get(id=invoice_id)

        # Send email logic
        send_mail(
            f'Invoice {invoice.invoice_number}',
            f'Details of invoice {invoice.invoice_number}',
            'from@example.com',
            [invoice.contact.email],
            fail_silently=False,
        )

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def add_service_contract(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)
    if request.method == 'POST':
        form = ServiceContractForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact_detail', contact_id=contact_id)
    else:
        form = ServiceContractForm()
    return render(request, 'contacts/contact_detail.html', {'form': form, 'contact': contact})

@require_POST
def create_checkout_session(request):
    invoice_id = request.POST.get('invoice_id')

    if not invoice_id:
        return redirect('cancel')

    invoice = get_object_or_404(Invoice, id=invoice_id)

    line_items = [{
        'price_data': {
            'currency': 'usd',
            'product_data': {
                'name': f'Invoice Total (including service fee)',
            },
            'unit_amount': int(invoice.total * 100),
        },
        'quantity': 1,
    }]

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri('/success/'),
        cancel_url=request.build_absolute_uri('/cancel/'),
    )

    return redirect(session.url, code=303)




def success(request):
    return render(request, 'success.html')

def cancel(request):
    return render(request, 'cancel.html')

def ajax_load_properties(request):
    contact_id = request.GET.get('contact_id')
    properties = Property.objects.filter(contact_id=contact_id).order_by('address')
    return JsonResponse({'properties': list(properties.values('id', 'address'))})

