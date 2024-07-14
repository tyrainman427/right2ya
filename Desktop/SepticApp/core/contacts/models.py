from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class Contact(models.Model):
    TYPE_CHOICES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
    ]
    CONTACT_METHOD_CHOICES = [
        ('phone', 'Phone'),
        ('email', 'Email'),
    ]

    contact_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    name = models.CharField(max_length=200,blank=True,null=True)
    address = models.CharField(max_length=255,blank=True,null=True)
    phone = models.CharField(max_length=15,blank=True,null=True)
    email = models.EmailField(max_length=100, blank=True,null=True)
    tank_amount = models.IntegerField(blank=True,null=True)
    tank_size = models.CharField(max_length=100,blank=True, null=True)
    auto_email = models.BooleanField(default=False)
    email_history = models.TextField(blank=True, null=True)
    preferred_contact_method = models.CharField(max_length=50, choices=CONTACT_METHOD_CHOICES, default="Phone")


    def __str__(self):
        return self.name

class Property(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="properties")
    address = models.CharField(max_length=255)
    township = models.CharField(max_length=100, blank=True, null=True)
    parcel_number = models.IntegerField(blank=True, null=True)
    permit_number = models.IntegerField(blank=True, null=True)
    payment_owed = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # Add more fields for estimates, service due notice, etc. as needed

    def __str__(self):
        return f"Property of {self.contact.name}"
    
class Document(models.Model):
    property = models.ForeignKey('Property', on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to='property_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document for {self.property.address}"
    
class PropertyImage(models.Model):
    property = models.ForeignKey('Property', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_images/')
    title = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Image for {self.property.address}"


class Payment(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='payments')
    date = models.DateField()
    invoice_number = models.CharField(max_length=100)
    description = models.TextField()
    invoice_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Invoice #{self.invoice_number} for {self.property.contact.name}"



class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()    
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 
    quantity = models.IntegerField(default=1)


    def __str__(self):
        return self.name

class Appointment(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateTimeField()
    job_volume = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='appointments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.service.name} on {self.date.strftime('%Y-%m-%d')}"

class Invoice(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='invoices')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='invoices')
    services = models.ManyToManyField(Service, related_name='invoices', blank=True)
    tech = models.CharField(max_length=100, null=True, blank=True) 
    date_of_service = models.DateTimeField()
    manifest_number = models.CharField(max_length=100, null=True, blank=True)
    invoice_number = models.CharField(max_length=10, unique=True, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,blank=True)
    
    is_paid = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)


        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invoice {self.invoice_number} for {self.contact.name}"


class ServiceContract(models.Model):
    FREQUENCY_CHOICES = [
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]

    job_name = models.CharField(max_length=100)
    total_tanks = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    service = models.TextField()
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)
    first_service_date = models.DateField()
    end_date = models.DateField()
    job_notes = models.TextField()

    def __str__(self):
        return f"{self.job_name} - {self.frequency}"

# class Service_Notice(models.Model):
# class Service_Notice(models.Model):
#     name = 
#     email_status = 
#     service_due_date = models
#     contact info 
#     job_code 

# class Manifest(models.Model):
#     contact
#     time_in =
#     time_out =
#     disposal_status = 
#     invoices =
#     disposal_notes = 
#     signature = 
    
# class Disposal(models.Model):
#     manifest = 
#     type = 
#     site_name = models
#     waste_type = 
#     del_date = models
#     completed = models
#     pump_vol