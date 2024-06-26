import requests
import stripe
import firebase_admin
from firebase_admin import credentials, auth, messaging
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseNotAllowed
from django.views.decorators.http import require_POST
from core.customer import forms
from core.forms import RestaurantForm
from stripe.error import CardError
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.conf import settings
from twilio.rest import Client
import random
import os
from core.models import *
from .utils import save
import psycopg2
from django.utils import timezone
from django.db.models import Q
from .forms import JobCreateStep1Form, JobCreateStep2Form, JobCreateStep3Form
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from decimal import Decimal



stripe.api_key = settings.STRIPE_API_SECRET_KEY

@login_required()
def home(request):
      
    return redirect(reverse('customer:profile'))

@login_required(login_url="/sign-in/?next=/customer/")
def profile_page(request):
    user_form = forms.BasicUserForm(instance=request.user)
    customer_form = forms.BasicCustomerForm(instance=request.user.customer)
    password_form = PasswordChangeForm(request.user)

    if request.method == "POST":

        if request.POST.get('action') == 'update_profile':
            user_form = forms.BasicUserForm(request.POST, instance=request.user)
            customer_form = forms.BasicCustomerForm(request.POST, request.FILES, instance=request.user.customer)

            if user_form.is_valid() and customer_form.is_valid():
                user_form.save()
                customer_form.save()

                messages.success(request, 'Your profile has been updated')
                return redirect(reverse('customer:profile'))

        elif request.POST.get('action') == 'update_password':
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)

                messages.success(request, 'Your password has been updated')
                return redirect(reverse('customer:profile'))

        elif request.POST.get('action') == 'update_phone':
            # Get Firebase user data
            firebase_user = auth.verify_id_token(request.POST.get('id_token'))

            request.user.customer.phone_number = firebase_user['phone_number']
            request.user.customer.save()
            return redirect(reverse('customer:profile'))

    return render(request, 'customer/profile.html', {
        "user_form": user_form,
        "customer_form": customer_form,
        "password_form": password_form
    })

@login_required(login_url="/sign-in/?next=/customer/")
def payment_method_page(request):
    current_customer = request.user.customer

    # Remove existing card
    if request.method == "POST":
        stripe.PaymentMethod.detach(current_customer.stripe_payment_method_id)
        current_customer.stripe_payment_method_id = ""
        current_customer.stripe_card_last4 = ""
        current_customer.save()
        return redirect(reverse('customer:payment_method'))

    # Save stripe customer infor
    if not current_customer.stripe_customer_id:
        customer = stripe.Customer.create()
        current_customer.stripe_customer_id = customer['id']
        current_customer.save()

    # Get Stripe payment method
    stripe_payment_methods = stripe.PaymentMethod.list(
        customer = current_customer.stripe_customer_id,
        type = "card",
    )

    print(stripe_payment_methods)

    if stripe_payment_methods and len(stripe_payment_methods.data) > 0:
        payment_method = stripe_payment_methods.data[0]
        current_customer.stripe_payment_method_id = payment_method.id
        current_customer.stripe_card_last4 = payment_method.card.last4
        current_customer.save()
    else:
        current_customer.stripe_payment_method_id = ""
        current_customer.stripe_card_last4 = ""
        current_customer.save()

    if not current_customer.stripe_payment_method_id:
        intent = stripe.SetupIntent.create(
            customer = current_customer.stripe_customer_id
        )

        return render(request, 'customer/payment_method.html', {
            "client_secret": intent.client_secret,
            "STRIPE_API_PUBLIC_KEY": settings.STRIPE_API_PUBLIC_KEY,
        })
    else:
        return render(request, 'customer/payment_method.html')

@login_required(login_url="/sign-in/?next=/customer/")
def create_job_page(request):
    current_customer = request.user.customer

    if not current_customer.stripe_payment_method_id:
        return redirect(reverse('customer:payment_method'))

    has_current_job = Job.objects.filter(
        customer=current_customer,
        status__in=[
            Job.PROCESSING_STATUS,
            Job.READY_STATUS,
            Job.PICKING_STATUS,
            Job.DELIVERING_STATUS,
            Job.SCHEDULED_STATUS,
        ]
    ).exists()

    creating_job = Job.objects.filter(customer=current_customer, status=Job.CREATING_STATUS).last()
    
    if creating_job:  # Check if creating_job is not None
        if request.POST.get('service_type') == 'scheduled':
            if creating_job.scheduled_date:
                creating_job.service_type = 'scheduled'
            else:
                creating_job.service_type = 'standard'

    
    
    step1_form = JobCreateStep1Form(instance=creating_job)
    step2_form = JobCreateStep2Form(instance=creating_job)
    step3_form = JobCreateStep3Form(instance=creating_job)

    if request.method == "POST":

        if request.POST.get('step') == '1':
            step1_form = JobCreateStep1Form(request.POST, request.FILES, instance=creating_job)
            if step1_form.is_valid():
                creating_job = step1_form.save(commit=False)
                creating_job.customer = current_customer
                creating_job.scheduled_date = step1_form.cleaned_data['scheduled_date']
                creating_job.save()
                return redirect(reverse('customer:create_job'))

        elif request.POST.get('step') == '2':
            step2_form = JobCreateStep2Form(request.POST, instance=creating_job)
            if step2_form.is_valid():
                creating_job.save()
                return redirect(reverse('customer:create_job'))

        elif request.POST.get('step') == '3':
            step3_form = JobCreateStep3Form(request.POST, instance=creating_job)
            if step3_form.is_valid():
                creating_job.save()

                try:
                    r = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json?&origins={}&destinations={}&mode=driving&best_guess&departure_time=now&region=us&units=imperial&key={}".format(
                        creating_job.pickup_address,
                        creating_job.delivery_address,
                        settings.GOOGLE_MAP_API_KEY,
                    ))

                    distance = r.json()['rows'][0]['elements'][0]['distance']['value']
                    duration = r.json()['rows'][0]['elements'][0]['duration']['value']
                    distance = round(distance / 1000, 2) * 0.62
                    creating_job.distance = distance
                    creating_job.duration = int(duration / 60)
                    creating_job.price = creating_job.calculate_price()
                    creating_job.save()

                except Exception as e:
                    print(e)
                    messages.error(request, "Unfortunately, we do not support shipping at this distance")

                return redirect(reverse('customer:create_job'))

        elif request.POST.get('step') == '4':
            if creating_job.price:
                try:
                    payment_intent = stripe.PaymentIntent.create(
                        amount=int(creating_job.price * 100),
                        currency='usd',
                        customer=current_customer.stripe_customer_id,
                        payment_method=current_customer.stripe_payment_method_id,
                        # capture_method='manual',
                        off_session=True,
                        confirm=True,
                    )
                    # Store the PaymentIntent ID in the Job instance
                    creating_job.stripe_payment_intent_id = payment_intent['id']
                    creating_job.save()

                    Transaction.objects.create(
                        stripe_payment_intent_id=payment_intent['id'],
                        job=creating_job,
                        amount=creating_job.price,
                        transaction_type=Transaction.JOB,
                    )
                    if creating_job.service_type == "scheduled":
                        creating_job.is_scheduled = True
                        creating_job.status = Job.SCHEDULED_STATUS
                    else:
                        creating_job.status = Job.PROCESSING_STATUS
                        
                    creating_job.paid_status = Job.PAID_STATUS
                    creating_job.save()

                    return redirect(reverse('customer:home'))

                except stripe.error.CardError as e:
                    err = e.error
                    payment_intent_id = err.payment_intent['id']
                    payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)

    # Determine the current step
    if not creating_job:
        current_step = 1
    elif creating_job.delivery_name:
        current_step = 4
    elif creating_job.pickup_name:
        current_step = 3
    else:
        current_step = 2

    return render(request, 'customer/create_job.html', {
        "job": creating_job,
        "step": current_step,
        "step1_form": step1_form,
        "step2_form": step2_form,
        "step3_form": step3_form,
        "GOOGLE_MAP_API_KEY": settings.GOOGLE_MAP_API_KEY,
    })

@login_required(login_url="/sign-in/?next=/customer/")
def current_jobs_page(request):
    current_date = timezone.localtime().date()
    jobs = Job.objects.filter(
        customer=request.user.customer,
        status__in=[
            Job.PROCESSING_STATUS,
            Job.READY_STATUS,
            Job.PICKING_STATUS,
            Job.DELIVERING_STATUS,
            Job.ARRIVED_STATUS,
            Job.SIGNED_STATUS,
            Job.SCHEDULED_STATUS,
        ]
    )
    
    for job in jobs:
        print(job.id, job.scheduled_date, job.status)  # This will print relevant fields for each job


    return render(request, 'customer/jobs.html', {
        "jobs": jobs,
    })

@login_required(login_url="/sign-in/?next=/customer/")
def archived_jobs_page(request):
    jobs = Job.objects.filter(
        customer=request.user.customer,
        status__in=[
            Job.COMPLETED_STATUS,
            Job.CANCELED_STATUS,
            Job.REVIEWED_STATUS
        ]
    )
    
    courier_id = [job.courier.id for job in jobs if job.courier is not None]


    return render(request, 'customer/jobs.html', {
        "jobs": jobs,
        "courier_id": courier_id
    })

@login_required(login_url="/sign-in/?next=/customer/")
def job_page(request, job_id):
    job = Job.objects.get(id=job_id)
    tip = Tip.objects.filter(job=job).first() 

    
    if request.method == "POST" and job.status == Job.READY_STATUS:
        job.status = Job.CANCELED_STATUS
        job.save()
        return redirect(reverse('customer:archived_jobs'))

    return render(request, 'customer/job.html', {
        "job": job,
        'tip': tip,
        "GOOGLE_MAP_API_KEY": settings.GOOGLE_MAP_API_KEY,
     
    })

@login_required
def select_job(request):
    if request.method == 'POST':
        delivery_choice = request.POST.get('delivery_choice')
        
        # Store the selected delivery choice in the session
        request.session['delivery_choice'] = delivery_choice

        if delivery_choice == Job.SAME_DAY_DELIVERY:
            return redirect('select_service_type')
        elif delivery_choice == Job.SCHEDULED_DELIVERY:
            return redirect('select_service_type')
    
    return render(request, 'customer/select_job.html')

@login_required
def select_service_type(request):
    if request.method == 'POST':
        service_type = request.POST.get('service_type')
        if service_type == 'standard':
            # Redirect to the standard service page (create_job view)
            return redirect('customer:create_job')
        elif service_type == 'scheduled':
            # Redirect to the scheduled service page (create_job view)
            return redirect('customer:create_job')

    # If the request method is not POST or the service type is not provided,
    # render the select service type template again
    return render(request, 'customer/select_job.html')

def choose_meal(request):
    if request.method == 'POST':
        meal_id = request.POST.get('meal_id')
        hours = request.POST.get('hours')

        # Retrieve the current customer
        current_customer = request.user.customer

        # Retrieve the selected meal
        meal = get_object_or_404(Meal, id=meal_id)

        # Calculate the total price based on the meal price and quantity
        meal_price = meal.price
        quantity = int(hours)
        total_price = meal_price * quantity

        # Create a new Job instance and set the meal, customer, and other fields
        job = Job()
        job.customer = current_customer
        job.service_type = 'standard'  # Set the service type accordingly
        job.quantity = quantity
        job.price = total_price
        # Set other job fields accordingly

        # Save the job instance
        job.save()

        # Redirect to the appropriate page with the price from the selected meal
        return redirect('customer:create', price=total_price)

    meals = Meal.objects.all()
    context = {
        'meals': meals,
    }
    return render(request, 'customer/services.html', context)

def job_summary(request, job_id):
    try:
        job = Job.objects.get(pk=job_id)
    except Job.DoesNotExist:
        return redirect('customer:create_job')

    return render(request, 'customer/job_summary.html', {'job': job})

def make_payment(request, job_id):
    try:
        job = Job.objects.get(pk=job_id)
    except Job.DoesNotExist:
        return redirect('customer:create_job')

    # Logic to create a payment intent and handle the payment process with Stripe
    # (You can use the existing code for this part)

    # After successful payment, send an email as a receipt
    send_mail(
        'Job Receipt',
        'Thank you for your payment. Here is the receipt for your job:\n\n' + str(job),
        'noreply@example.com',
        [job.customer.email],
        fail_silently=False,
    )

    # Redirect to a thank you page after successful payment
    return redirect('customer:home')

def get_default_card(customer_id):
    customer = stripe.Customer.retrieve(customer_id)
    if 'default_source' in customer and customer['default_source'] is not None:
        card = stripe.Customer.retrieve_source(
            customer_id,
            customer['default_source'],
        )
        return card
    else:
        return None


def add_tip(request, job_id):
    current_customer = request.user.customer
    job = get_object_or_404(Job, pk=job_id)
    
    if request.method == 'POST':
        form = forms.AddTipForm(request.POST)
        
        if form.is_valid():
            tip_amount = form.cleaned_data['tip']
            
            # 1. Create a Tip instance and link it to the job
            tip = Tip.objects.create(job=job, amount=tip_amount)
            job.tipped = tip
            job.save()
            
            # 2. Retrieve the Stripe details of the customer
            stripe_customer_id = current_customer.stripe_customer_id
            stripe_payment_method_id = current_customer.stripe_payment_method_id
            
            # 3. Calculate the total price with the tip
            job_price_decimal = Decimal(str(job.price))
            total_price_with_tip = job_price_decimal + job.tipped.amount

            # 4. Refund the original payment intent
            stripe.Refund.create(
                payment_intent=job.stripe_payment_intent_id,
            )

            # 5. Create a new Stripe PaymentIntent with the tip included
            new_payment_intent = stripe.PaymentIntent.create(
                amount=int(total_price_with_tip * 100),  # Convert to cents
                currency='usd',
                customer=stripe_customer_id,
                payment_method=stripe_payment_method_id,
                confirm=True,
            )

            # 6. Update the job with the new Stripe PaymentIntent ID
            job.stripe_payment_intent_id = new_payment_intent['id']
            job.save()

            # 7. Create a new Transaction for the tip
            Transaction.objects.create(
                stripe_payment_intent_id=new_payment_intent['id'],
                job=job,
                tip=tip.amount,
                transaction_type=Transaction.TIP,
                amount=tip_amount,
            )

            # 8. Redirect to the job page
            return redirect('customer:job', job_id=job.id)

        else:
            messages.error(request, "Invalid form data.")
    else:
        form = forms.AddTipForm()

    return render(
        request, 
        'customer/add_tip.html', 
        {'form': form, 'job': job, 'total_price_with_tip': job.price}
    )


@login_required
@require_POST
def cancel_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if job.customer.user != request.user or job.status != 'processing':
        return HttpResponseNotAllowed('Cannot cancel this job')

    job.status = 'canceled'
    job.save()

    return redirect('customer:home') 