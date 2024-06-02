from django.db import models
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Client(models.Model):
    first_name= models.CharField(max_length=255)
    last_name= models.CharField(max_length=255, blank=True,null=True)
    address= models.CharField(max_length=255)
    phone= models.CharField(max_length=10)
    date_of_birth = models.CharField(max_length=10)
    client_id = models.IntegerField()
    medicaid_id = models.IntegerField()
    csp_contact_info = models.CharField(max_length=255)
    referring_clinician = models.CharField(max_length=255)
    cop_name_and_number = models.CharField(max_length=255)
    service_days = models.CharField(max_length=255)
    service_hours = models.CharField(max_length=255)
    intake_completed_by = models.CharField(max_length=255)
    date = models.CharField(max_length=255)
    start_date = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse('clients:file_detail', args=[str(self.id)])


class Document(models.Model):
    client = models.ForeignKey(Client,on_delete=models.CASCADE, related_name='documents')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    title = models.CharField(max_length=50)
    docs = models.FileField()

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse('clients:clients_list')

class Note(models.Model):
    client = models.ForeignKey(Client,on_delete=models.CASCADE, related_name='notes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    title = models.CharField(max_length=50)
    note = models.TextField(max_length=500)

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse('clients:clients_list')
