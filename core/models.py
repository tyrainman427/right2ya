import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.crypto import get_random_string
from datetime import datetime, timedelta

# Create your models here.
class Restaurant(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='restaurant')
  name = models.CharField(max_length=255)
  phone = models.CharField(max_length=255)
  address = models.CharField(max_length=255)
  logo = models.ImageField(upload_to='rest_images',blank=True,null=True)

  def __str__(self):
    return self.name
  
class Meal(models.Model):
  restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='restaurant')
  name = models.CharField(max_length=255)
  short_description = models.TextField(max_length=500)
  image = models.ImageField(upload_to='service_images',blank=True,null=True)
  price = models.IntegerField(default=0)


class Customer(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer',)
  avatar = models.ImageField(upload_to='customer/avatars/', blank=True, null=True)
  address = models.CharField(max_length=255, blank=True)
  phone_number = models.CharField(max_length=50, blank=True)
  stripe_customer_id = models.CharField(max_length=255, blank=True)
  stripe_payment_method_id = models.CharField(max_length=255, blank=True)
  stripe_card_last4 = models.CharField(max_length=255, blank=True)
  is_customer = models.BooleanField(default=True)


  def __str__(self):
    return self.user.get_full_name()

class Courier(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='courier',)
  lat = models.FloatField(default=0)
  lng = models.FloatField(default=0)
  #temp to fix location bug
  location = models.CharField(max_length=255, blank=True)
  paypal_email = models.EmailField(max_length=255, blank=True)
  fcm_token = models.TextField(blank=True)
  
  car_make = models.CharField(max_length=255, blank=True)
  car_model = models.CharField(max_length=255, blank=True)
  plate_number = models.CharField(max_length=255, blank=True)
  is_available = models.BooleanField(default=False)
  is_courier = models.BooleanField(default=True)
  average_rating = models.FloatField(default=0)  # Field to store the average rating
  total_reviews = models.IntegerField(default=0) 
  
  def calculate_average_rating(self):
        if self.total_reviews > 0:
            average = self.ratings.aggregate(models.Avg('rating_value'))['rating_value__avg']
            self.average_rating = round(average, 2)
        else:
            self.average_rating = 0
            self.save()

  def __str__(self):
    return self.user.get_full_name()
  
class Rating(models.Model):
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE, related_name='ratings')
    rating_value = models.IntegerField(default=0)
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.courier.total_reviews = self.courier.ratings.count()
        self.courier.average_rating = self.courier.ratings.aggregate(models.Avg('rating_value'))['rating_value__avg']
        self.courier.save()

    def __str__(self):
        return f"Rating: {self.rating_value} - Courier: {self.courier}"
      

class Category(models.Model):
  slug = models.CharField(max_length=255, unique=True)
  name = models.CharField(max_length=255)

  def __str__(self):
    return self.name

class Job(models.Model):
  SMALL_SIZE = "small"
  MEDIUM_SIZE = "medium"
  LARGE_SIZE = "large"
  SIZES = (
    (SMALL_SIZE, 'Small'),
    (MEDIUM_SIZE, 'Medium'),
    (LARGE_SIZE, 'Large'),
  )
  SAME_DAY_DELIVERY = 'same_day'
  SCHEDULED_DELIVERY = 'scheduled'
  SERVICE_DELIVERY = 'services'
  
  SERVICE_DELIVERY = (
        ('standard', 'Standard Delivery'),
        ('scheduled', 'Scheduled Delivery'),
        ('services', 'Services'),
    )

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
    (READY_STATUS, 'ready'),
    (PICKING_STATUS, 'Picking'),
    (DELIVERING_STATUS, 'Delivering'),
    (COMPLETED_STATUS, 'Completed'),
    (REVIEWED_STATUS, 'reviewed'),
    (CANCELED_STATUS, 'Canceled'),
  )

  # Step 1
  id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
  customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
  meal = models.ForeignKey(Meal, on_delete=models.CASCADE, null=True, blank=True)
  courier = models.ForeignKey(Courier, on_delete=models.CASCADE, null=True, blank=True)
  name = models.CharField(max_length=255)
  description = models.CharField(max_length=255)
  category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
  size = models.CharField(max_length=20, choices=SIZES, default=MEDIUM_SIZE)
  quantity = models.IntegerField(default=1)
  photo = models.ImageField(upload_to='job/photos/',null=True,blank=True)
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
  service_type = models.CharField(choices=SERVICE_DELIVERY, default='standard', max_length=20)
  meal_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
  rated = models.BooleanField(default=False)
  

  def save(self, *args, **kwargs):
    if self.delivery_date_time and self.delivery_time:
        pickup_datetime = datetime.combine(self.delivery_date_time, self.delivery_time)
        pickup_datetime = timezone.make_aware(pickup_datetime, timezone.get_current_timezone())  # Convert to offset-aware datetime

        current_datetime = timezone.now()

        # Display the job on the map one hour before the pickup time
        if pickup_datetime - current_datetime <= timedelta(hours=1):
            self.status = self.READY_STATUS
            self.calculate_price()  # Recalculate price for display

    else:
        self.status = self.CREATING_STATUS
        self.calculate_price()  # Calculate price for non-scheduled delivery

    super().save(*args, **kwargs)


  def calculate_price(self):
        # Pricing logic for scheduled delivery
        if self.delivery_date_time and self.delivery_time:
            self.service_fee = self.price
            self.delivery_fee = 0.25 * self.service_fee
        # Pricing logic for services with a selected meal
        elif self.service_type == 'services' and self.meal is not None:
            self.service_fee = self.meal.price
            self.price = self.service_fee
            self.delivery_fee = 0.25 * self.service_fee
        # Pricing logic for same day delivery
        else:
            self.service_fee = self.price - (self.price * 0.25)
            self.delivery_fee = 0.25 * self.price

  def __str__(self):
      return f"{self.name}"

class Transaction(models.Model):
  IN_STATUS = "in"
  OUT_STATUS = "out"
  STATUSES = (
    (IN_STATUS, 'In'),
    (OUT_STATUS, 'Out'),
  )

  stripe_payment_intent_id = models.CharField(max_length=255, unique=True)
  job = models.ForeignKey(Job, on_delete=models.CASCADE)
  amount = models.FloatField(default=0)
  status = models.CharField(max_length=20, choices=STATUSES, default=IN_STATUS)
  created_at = models.DateTimeField(default=timezone.now)

  def __str__(self):
    return self.stripe_payment_intent_id


class Dashboard(models.Model):
  jobs = models.ForeignKey(Job, on_delete=models.CASCADE)
  couriers = models.ForeignKey(Courier,on_delete=models.CASCADE)
  customers = models.ForeignKey(Customer, on_delete=models.CASCADE)
  
  def __str__(self):
    return self.jobs.name
      


  def __str__(self):
    return self.name    

class Order(models.Model):
  PROCESSING = 1
  READY = 2
  ONTHEWAY = 3
  DELIVERED = 4

  STATUS_CHOICES = (
    (PROCESSING, "Processing"),
    (READY, "Ready"),
    (ONTHEWAY, "On the way"),
    (DELIVERED, "Delivered"),
  )

  customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
  restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT)
  courier = models.ForeignKey(Courier, models.SET_NULL, blank=True, null=True)
  address = models.CharField(max_length=500)
  total = models.IntegerField()
  status = models.IntegerField(choices=STATUS_CHOICES)
  created_at = models.DateTimeField(default=timezone.now)
  picked_at = models.DateTimeField(blank=True, null=True)

  def __str__(self):
    return str(self.id)

class OrderDetails(models.Model):
  order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='order_details')
  meal = models.ForeignKey(Meal, on_delete=models.PROTECT)
  quantity = models.IntegerField()
  sub_total = models.IntegerField()

  def __str__(self):
    return str(self.id)


