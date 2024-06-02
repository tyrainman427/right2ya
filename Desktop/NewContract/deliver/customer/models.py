from django.db import models

# Create your models here.
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='menu_images/')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ManyToManyField('Category', related_name='item')
    
    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class OrderModel(models.Model):
    METHOD_OF_PAYMENT = (
        ('Cash','Cash'),
        ('Zelle','Zelle'),
        ('Cashapp','Cashapp'),
        ('Venmo','Venmo'),
    )
    TYPE_OF_PAYMENT = (
        ('Advance Payment Deposit','Advance Payment Deposit'),
        ('Full Amount','Full Amount'),
    )
    
    created_on = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    items = models.ManyToManyField('MenuItem', related_name='order',blank=True)
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
    type_of_payment = models.CharField(max_length=50,choices=TYPE_OF_PAYMENT, default="Advance Payment Deposit")
    method_of_payment = models.CharField(max_length=50, choices=METHOD_OF_PAYMENT, default="Cash")
    is_paid = models.BooleanField(default=False)
    is_completed= models.BooleanField(default=False)
    
    def __str__(self):
        return f'Order: {self.created_on.strftime("%b %d %I: %M %p")}'