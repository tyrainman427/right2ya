from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from django.utils import timezone
from decimal import Decimal
import uuid

from core.models import *


class ScheduledJob(models.Model):
    CREATING_STATUS = 'creating'
    PROCESSING_STATUS = 'processing'
    READY_STATUS = 'ready'
    PICKING_STATUS = 'picking'
    DELIVERING_STATUS = 'Delivering Order'
    COMPLETED_STATUS = 'completed'
    REVIEWED_STATUS = 'reviewed'
    CANCELED_STATUS = 'canceled'
    STATUSES = (
        (CREATING_STATUS, 'Creating'),
        (PROCESSING_STATUS, 'Processing'),
        (READY_STATUS, 'Ready'),
        (PICKING_STATUS, 'Picking'),
        (DELIVERING_STATUS, 'Delivering'),
        (COMPLETED_STATUS, 'Completed'),
        (REVIEWED_STATUS, 'Reviewed'),
        (CANCELED_STATUS, 'Canceled'),
    )
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    photo = models.ImageField(upload_to='job/photos/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUSES, default=CREATING_STATUS)
    created_at = models.DateTimeField(default=timezone.now)

    # Step 2
    pickup_address = models.CharField(max_length=255, blank=True)
    pickup_lat = models.FloatField(default=0)
    pickup_lng = models.FloatField(default=0)
    pickup_name = models.CharField(max_length=255, blank=True)
    pickup_phone = models.CharField(max_length=50, blank=True)

    # Step 3
    delivery_address = models.CharField(max_length=255, blank=True)
    delivery_lat = models.FloatField(default=0)
    delivery_lng = models.FloatField(default=0)
    delivery_name = models.CharField(max_length=255, blank=True)
    delivery_phone = models.CharField(max_length=50, blank=True)

    # Step 4
    duration = models.IntegerField(default=0)
    distance = models.FloatField(default=0)
    price = models.FloatField(default=0)

    # Extra info
    pickup_photo = models.ImageField(upload_to='job/pickup_photos/', null=True, blank=True)
    pickedup_at = models.DateTimeField(null=True, blank=True)

    delivery_photo = models.ImageField(upload_to='job/delivery_photos/', null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    delivery_date_time = models.DateField(blank=True, null=True)
    delivery_time = models.TimeField(blank=True, null=True)

    # Pricing
    service_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    delivery_fee = models.FloatField(default=0)
    scheduled_datetime = models.DateTimeField()

    def __str__(self):
        return f"Scheduled Job #{self.id} for {self.customer.username}"

    def save(self, *args, **kwargs):
        if self.scheduled_datetime:
            current_datetime = timezone.now()

            if self.scheduled_datetime - current_datetime <= timedelta(hours=1):
                self.status = self.READY_STATUS
                self.calculate_price()

        else:
            self.calculate_price()

        super().save(*args, **kwargs)

    def calculate_price(self):
        self.service_fee = self.price
        self.delivery_fee = 0.25 * self.service_fee + 3.99
