from django.db import models

# Create your models here.
class Contract(models.Model):
    client_full_name = models.CharField(max_length=75,blank=False,null=False)
    contact_person = models.CharField(max_length=50,blank=False,null=False)
    address = models.CharField(max_length=200,blank=False,null=False)
    city = models.CharField(max_length=75,blank=False,null=False)
    state = models.CharField(max_length=2,blank=False,null=False)
    zip_code = models.CharField(max_length=5,blank=False,null=False) 
    telephone_number = models.CharField(max_length=10,blank=False,null=False)
    cell_number = models.CharField(max_length=10,blank=False,null=False)
    email = models.EmailField(null=False,blank=False)
    date_of_event = models.CharField(max_length=50,blank=False,null=False)
    event_type = models.CharField(max_length=50,blank=False,null=False)
    number_of_guests = models.CharField(max_length=3,blank=False,null=False)
    start_time = models.CharField(max_length=50,blank=False,null=False)
    end_time = models.CharField(max_length=50,blank=False,null=False)
    location_of_event = models.CharField(max_length=50,blank=False,null=False)
    phone_number = models.CharField(max_length=10,blank=False,null=False)
    add_photos = models.BooleanField(default=False)
    add_lights = models.BooleanField(default=False)
    add_more_time = models.BooleanField(default=False)
    add_visuals_on_HD = models.BooleanField
    type_of_payment = models.CharField(max_length=50,blank=False,null=False)
    method_of_payment = models.CharField(max_length=50,blank=False,null=False)
    total_price = models.IntegerField(blank=False,null=True)
    
    def __str__(self):
        return self.client_full_name