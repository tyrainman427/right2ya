from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ScheduledJobForm
import stripe
from core.models import *
from .models import *
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import *
import requests
from core.models import Transaction

stripe.api_key = settings.STRIPE_API_SECRET_KEY


@csrf_exempt
@login_required
def create_job(request):
    current_customer = request.user.customer

    if not current_customer.stripe_payment_method_id:
        return redirect(reverse('customer:payment_method'))

    has_current_job = ScheduledJob.objects.filter(
        customer=current_customer,
        status__in=[
            Job.PROCESSING_STATUS,
            Job.PICKING_STATUS,
            Job.DELIVERING_STATUS
        ]
    ).exists()

    # if has_current_job:
    #     messages.warning(request, "You currently have a processing job.")
    #     return redirect(reverse('customer:current_jobs'))

    creating_job = ScheduledJob.objects.filter(customer=current_customer, status=ScheduledJob.CREATING_STATUS).last()
    step1_form = JobCreateStep1Form(instance=creating_job)
    step2_form = JobCreateStep2Form(instance=creating_job)
    step3_form = JobCreateStep3Form(instance=creating_job)

    if request.method == "POST":
        if request.POST.get('step') == '1':
            step1_form = JobCreateStep1Form(request.POST, request.FILES, instance=creating_job)
            if step1_form.is_valid():
                creating_job = step1_form.save(commit=False)
                creating_job.customer = current_customer
                creating_job.save()
                return redirect(reverse('scheduler:create_job'))

        elif request.POST.get('step') == '2':
            step2_form = JobCreateStep2Form(request.POST, instance=creating_job)
            if step2_form.is_valid():
                creating_job = step2_form.save()
                return redirect(reverse('scheduler:create_job'))

        elif request.POST.get('step') == '3':
            step3_form = JobCreateStep3Form(request.POST, instance=creating_job)
            if step3_form.is_valid():
                creating_job = step3_form.save()

                try:
                    r = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json?&origins={}&destinations={}&mode=driving&best_guess&departure_time=now&region=us&units=imperial&key={}".format(
                        creating_job.pickup_address,
                        creating_job.delivery_address,
                        settings.GOOGLE_MAP_API_KEY,
                    ))

                    print(r.json()['rows'])

                    distance = r.json()['rows'][0]['elements'][0]['distance']['value']
                    duration = r.json()['rows'][0]['elements'][0]['duration']['value']
                    distance = round(distance / 1000, 2) * 0.62
                    creating_job.distance = distance
                    creating_job.duration = int(duration / 60)
                    creating_job.price = round(creating_job.distance * 1.5 + 3.99, 2)  # $1.50 per mile
                    creating_job.save()

                except Exception as e:
                    print(e)
                    messages.error(request, "Unfortunately, we do not support shipping at this distance")

                return redirect(reverse('scheduler:create_job'))
        elif request.POST.get('step') == '4':
            if creating_job.price:
                try:
                    payment_intent = stripe.PaymentIntent.create(
                        amount=int(creating_job.price * 100),
                        currency='usd',
                        customer=current_customer.stripe_customer_id,
                        payment_method=current_customer.stripe_payment_method_id,
                        off_session=True,
                        confirm=True,
                    )

                    Transaction.objects.create(
                        stripe_payment_intent_id = payment_intent['id'],
                        job = creating_job,
                        amount = creating_job.price,
                    )

                    creating_job.status = ScheduledJob.PROCESSING_STATUS
                    creating_job.save()


                    return redirect(reverse('customer:home'))

                except ScheduledJob.DoesNotExist:
                    messages.error(request, "Invalid job.")
                    return redirect(reverse('scheduler:create_job'))

        else:
            messages.error(request, "No meal selected.")
            return redirect(reverse('scheduler:create_job'))

    # Determine the current step
    if not creating_job:
        current_step = 1
    elif creating_job.delivery_name:
        current_step = 4
    elif creating_job.pickup_name:
        current_step = 3
    else:
        current_step = 2

    return render(request, 'scheduler/create_job.html', {
        "job": creating_job,
        "step": current_step,
        "step1_form": step1_form,
        "step2_form": step2_form,
        "step3_form": step3_form,
        "GOOGLE_MAP_API_KEY": settings.GOOGLE_MAP_API_KEY
    })




    # return render(request, 'scheduler/create_scheduled_job.html', {'form': form,"GOOGLE_MAP_API_KEY": settings.GOOGLE_MAP_API_KEY,})


def view_scheduled_jobs(request):
    scheduled_jobs = ScheduledJob.objects.filter(customer=request.user)
    context = {'scheduled_jobs': scheduled_jobs}
    return render(request, 'scheduler/view_scheduled_jobs.html', context)

def payment_confirmation(request):
    return render(request, 'scheduler/payment_confirmation.html')

@login_required
def job_confirmation(request, job_id):
    job = Job.objects.get(id=job_id)

    return render(request, 'core/job_confirmation.html', {'job': job})

