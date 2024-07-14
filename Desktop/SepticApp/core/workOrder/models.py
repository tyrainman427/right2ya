from django.db import models
from contacts.models import Property, Contact, Service

class WorkOrder(models.Model):
    ADDRESS_CONFIRMATION_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('unsure', 'Unsure'),
    ]

    DRIVEWAY_EVALUATION_CHOICES = [
        ('safe', 'Safe to back in'),
        ('avoid', 'Avoid'),
    ]

    COVER_CONDITION_CHOICES = [
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('bad', 'Bad'),
    ]

    FLUID_LEVEL_CHOICES = [
        ('normal', 'Normal'),
        ('high', 'High'),
        ('low', 'Low'),
    ]

    # other fields such as customer, date, etc. can be added here
    work_order_number = models.CharField(max_length=50, blank=True, null=True, default=3000)
    verify_address = models.CharField(max_length=50, choices=ADDRESS_CONFIRMATION_CHOICES)
    evaluate_driveway = models.CharField(max_length=50, choices=DRIVEWAY_EVALUATION_CHOICES)
    cover_condition = models.CharField(max_length=50, choices=COVER_CONDITION_CHOICES)
    fluid_level = models.CharField(max_length=50, choices=FLUID_LEVEL_CHOICES)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='work_orders', null=True, blank=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='work_orders', null=True, blank=True)
    services = models.ManyToManyField(Service, related_name='work_orders', blank=True)  # Changed to ManyToManyField
    date_of_service = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    is_completed = models.BooleanField(default=False)



    def __str__(self):
        return f"Work Order #{self.id}"  # or any other meaningful string representation
