from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from core.serializers import JobSerializer
from core.models import *
from .forms import *
from rest_framework import generics
from core.views import *

@login_required(login_url="/sign-in/?next=/courier/")
def home(request):
    return redirect(reverse('courier:onboarding_welcome'))

@login_required
def onboarding_welcome(request):
    return render(request,'courier/onboarding_welcome.html')

@login_required
def onboarding_steps(request):
    return render(request,'courier/onboarding_steps.html')

@login_required
def onboarding_safety(request):
    return render(request,'courier/onboarding_safety.html')


@login_required(login_url="/sign-in/?next=/courier/")
def available_jobs_page(request):
    print("This code is running")
    job = Job.objects.filter(status=Job.READY_STATUS).last()
    courier = request.user.courier

    if job is None:
        pass
    print(job)
    return render(request, 'courier/available_jobs.html', {
        "GOOGLE_MAP_API_KEY": settings.GOOGLE_MAP_API_KEY,
         "job": job,
        "courier": courier,
    })

@login_required(login_url="/sign-in/?next=/courier/")
def available_job_page(request, id):
    job = Job.objects.filter(id=id, status=Job.READY_STATUS).last()
    print("Job:",job)

    if not job:
        return redirect(reverse('courier:available_jobs'))

    if request.method == 'POST':
        job.courier = request.user.courier
        job.status = Job.PICKING_STATUS
        job.save()
        update_templates_and_publish(job.id,job.status)

        try:
            layer = get_channel_layer()
            async_to_sync(layer.group_send)("job_" + str(job.id), {
                'type': 'job_update',
                'job': {
                    'status': job.get_status_display(),
                }
            })
        except:
            pass

        return redirect(reverse('courier:available_jobs'))

    return render(request, 'courier/available_job.html', {
        "job": job,
 
    })

@login_required(login_url="/sign-in/?next=/courier/")
def current_job_page(request):
    job = Job.objects.filter(
        courier=request.user.courier,
        status__in = [
            Job.PICKING_STATUS,
            Job.DELIVERING_STATUS
        ]
    ).last()

    return render(request, 'courier/current_job.html', {
        "job": job,
        "GOOGLE_MAP_API_KEY": settings.GOOGLE_MAP_API_KEY
    })

@login_required(login_url="/sign-in/?next=/courier/")
def current_job_take_photo_page(request, id):
    job = Job.objects.filter(
        id=id,
        courier=request.user.courier,
        status__in=[
            Job.PICKING_STATUS,
            Job.DELIVERING_STATUS
        ]
    ).last()

    if not job:
        return redirect(reverse('courier:current_job'))

    return render(request, 'courier/current_job_take_photo.html', {
        "job": job
    })

@login_required(login_url="/sign-in/?next=/courier/")
def job_complete_page(request):

    return render(request, 'courier/job_complete.html')

@login_required(login_url="/sign-in/?next=/courier/")
def archived_jobs_page(request):
    jobs = Job.objects.filter(
        courier=request.user.courier,
        status=Job.COMPLETED_STATUS
    )

    return render(request, 'courier/archived_jobs.html', {
        "jobs": jobs
    })

@login_required(login_url="/sign-in/?next=/courier/")
def profile_page(request):
    jobs = Job.objects.filter(
        courier=request.user.courier,
        status__in=[Job.COMPLETED_STATUS, Job.REVIEWED_STATUS]
    )
    courier = request.user.courier

    total_earnings = round(sum(job.price for job in jobs) * 0.75, 2)
    total_jobs = len(jobs)
    total_km = sum(job.distance for job in jobs)

    return render(request, 'courier/profile.html', {
        "total_earnings": total_earnings,
        "total_jobs": total_jobs,
        "total_km": total_km,
        "courier": courier
    })

@login_required(login_url="/sign-in/?next=/courier/")
def payout_method_page(request):
    payout_form = forms.PayoutForm(instance=request.user.courier)

    if request.method == 'POST':
        payout_form = forms.PayoutForm(request.POST, instance=request.user.courier)
        if payout_form.is_valid():
            payout_form.save()

            messages.success(request, "Payout address is updated.")
            return redirect(reverse('courier:profile'))

    return render(request, 'courier/payout_method.html', {
        'payout_form': payout_form
    })

class JobList(generics.ListCreateAPIView):
    queryset = Job.objects.filter(status=Job.READY_STATUS)
    serializer_class = JobSerializer
    

class JobDetailList(generics.RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

from django.views.decorators.http import require_http_methods

@require_http_methods(["GET", "POST"]) 
@login_required
def update_switch_state(request):
    if request.method == 'POST':
        is_available = request.POST.get('is_available')
        courier = request.user.courier
        print("ID: ", courier.id)

        # Update the switch state of the courier
        courier.is_available = is_available
        courier.save()

        return JsonResponse({'message': 'Switch state updated successfully.'})

    return JsonResponse({'message': 'Invalid request method.'}, status=400)
