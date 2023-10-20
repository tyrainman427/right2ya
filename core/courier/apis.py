from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from stripe.error import StripeError


from core.models import *

@csrf_exempt
@login_required(login_url="/courier/sign-in/")
def available_jobs_api(request):
  jobs = list(Job.objects.filter(status=Job.READY_STATUS).values())
  print("Jobs:",jobs)

  return JsonResponse({
    "success": True,
    "jobs": jobs
  })

@csrf_exempt
@login_required(login_url="/courier/sign-in/")
def current_job_update_api(request, id):
  job = Job.objects.filter(
    id=id,
    courier=request.user.courier,
    status__in=[
      Job.PICKING_STATUS,
      Job.DELIVERING_STATUS,
      Job.SIGNED_STATUS,
      Job.ARRIVED_STATUS,
    ]
  ).last()

  if job.status == Job.PICKING_STATUS:
    job.pickup_photo = request.FILES['pickup_photo']
    job.pickedup_at = timezone.now()
    job.status = Job.DELIVERING_STATUS
    job.save()

    print(job.pickup_photo.url)

    try:
      layer = get_channel_layer()
      async_to_sync(layer.group_send)("job_" + str(job.id), {
        'type': 'job_update',
        'job': {
          'status': job.get_status_display(),
          'pickup_photo': job.pickup_photo.url,
        }
      })
    except:
      pass

  elif job.status == Job.SIGNED_STATUS:
      job.delivery_photo = request.FILES['delivery_photo']
      job.delivered_at = timezone.now()
      job.status = Job.COMPLETED_STATUS
      job.save()

      # Handle the tip here
      tip_amount = 0  # Retrieve this from your frontend or some other way
      if tip_amount > 0:
          total_amount_to_charge = job.price + tip_amount
          try:
              # Refund the original charge first
              stripe.Refund.create(
                  payment_intent=job.stripe_payment_intent_id,
              )
              
              # Create a new PaymentIntent with the new total amount
              new_payment_intent = stripe.PaymentIntent.create(
                  amount=int(total_amount_to_charge * 100),
                  currency='usd',
                  customer=job.customer.stripe_customer_id,
                  payment_method=job.customer.stripe_payment_method_id,
                  capture_method='manual',
                  off_session=True,
                  confirm=True,
              )

              # Update the job with the new PaymentIntent ID
              job.stripe_payment_intent_id = new_payment_intent['id']
              job.save()

              async_to_sync(layer.group_send)("job_" + str(job.id), {
                  'type': 'job_update',
                  'job': {
                      'status': job.get_status_display(),
                      'payment_status': 'Payment successful',
                  }
              })
          except StripeError as e:
              async_to_sync(layer.group_send)("job_" + str(job.id), {
                  'type': 'job_update',
                  'job': {
                      'status': job.get_status_display(),
                      'payment_status': f'Payment failed: {str(e)}',
                  }
              })

      # The rest of your existing code
      try:
          layer = get_channel_layer()
          async_to_sync(layer.group_send)("job_" + str(job.id), {
              'type': 'job_update',
              'job': {
                  'status': job.get_status_display(),
                  'delivery_photo': job.delivery_photo.url,
              }
          })
      except:
          pass

  return JsonResponse({
    "success": True
  })

@csrf_exempt
@login_required(login_url="/courier/sign-in/")
def fcm_token_update_api(request):
  request.user.courier.fcm_token = request.GET.get('fcm_token')
  request.user.courier.save()

  return JsonResponse({
    "success": True
  })
