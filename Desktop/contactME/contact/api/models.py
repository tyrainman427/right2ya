from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.conf import settings
from datetime import date


class User(AbstractBaseUser):
  username = models.CharField(max_length = 50, blank = True, null = True, unique = True)
  email = models.EmailField(unique = True)
  native_name = models.CharField(max_length = 5)
  phone_no = models.CharField(max_length = 10)
  USERNAME_FIELD = 'username'
  REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
  RELATED_NAME = 'email'
  def __str__(self):
      return "{}".format(self.email)

# Create your models here.
class ContactUser(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    address = models.CharField(max_length=250,blank=False)
    email = models.EmailField()
    phone = models.IntegerField()
    isPrivate = models.BooleanField(default=False)
    owner = models.ForeignKey('auth.User', related_name='contactUsers', on_delete=models.CASCADE)
    

    class Meta:
        ordering = ['last_name']

    def __str__(self):
        return self.first_name