

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils import timezone
import core.models
from django.contrib import messages

import json
import requests

@csrf_exempt
def update_order_status(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')
        
        # Update the order status in the database
        new_order = core.models.Order()
        order = new_order.objects.get(id=order_id)
        order.status = new_status
        order.save()

        # Send a push notification to the user
        device_token = order.user.device_token
        message = {
            "to": device_token,
            "notification": {
                "title": "Order Status Updated",
                "body": f"Your order status has been updated to {new_status}",
                "sound": "default"
            }
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"key={settings.FIREBASE_API_KEY}"
        }
        response = requests.post("https://fcm.googleapis.com/fcm/send", data=json.dumps(message), headers=headers)
        
        if response.status_code == 200:
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=500)
    else:
        messages.failure(request, 'Order status was not updated.')
        
        return HttpResponse(status=405)