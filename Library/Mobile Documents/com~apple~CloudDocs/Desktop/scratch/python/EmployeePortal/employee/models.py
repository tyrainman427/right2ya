from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import datetime
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Custom related_name
        blank=True,
        help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_query_name='customuser',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Custom related_name
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_query_name='customuser',
    )

    def __str__(self):
        return self.email

YEARS_COMPLETED = (
    ("9","9"),
    ("10","10"),
    ("11","11"),
    ("12","12"),
)



class Employee(models.Model):
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)

    first_name= models.CharField(max_length=255)
    last_name= models.CharField(max_length=255)
    address= models.CharField(max_length=255)
    email= models.EmailField(max_length=100,blank=True,null=True)
    phone= models.CharField(max_length=10)
    us_citizen= models.BooleanField(default=False)
    over18= models.BooleanField(default=False)
    dob= models.DateField(null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=5)
    title = models.CharField(max_length=30, blank=True)
    department = models.CharField(max_length=50)
    work_location = models.CharField(max_length=50)
    supervisor = models.CharField(max_length=50)
    emergency_contact_name = models.CharField(max_length=50)
    emergency_contact_number = models.CharField(max_length=50)
    salary = models.FloatField(default=0.00, blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    # exclude below
    date_hired=models.DateField(null=True)
    # exclude above
    been_convicted= models.BooleanField(default=False)
    explain_conviction=models.TextField(blank=True,null=True)
    military_service= models.BooleanField(default=False)
    branch= models.CharField(max_length=100,blank=True,null=True)
    veteran= models.BooleanField(default=False)
    position_applying= models.CharField(max_length=255,blank=True,null=True)
    how_Did_You_Hear_About_Position= models.CharField(max_length=255,blank=True,null=True)
    expected_rate= models.FloatField(blank=True,null=True)
    expect_weekly_rate= models.FloatField(blank=True,null=True)
    date_available= models.DateField(null=True)
    resume= models.FileField(blank=True,null=True)
    social_security= models.FileField(blank=True,null=True)
    gov_id= models.FileField(blank=True,null=True)
    # education
    high_school= models.CharField(max_length=255,blank=True,null=True)
    last_year_completed = models.CharField(max_length=2,choices=YEARS_COMPLETED,default="9")
    graduated= models.BooleanField(default=False)
    college= models.CharField(max_length=255,blank=True,null=True)
    last_college_Year_completed = models.CharField(default="9",max_length=2,choices=YEARS_COMPLETED)
    major= models.CharField(max_length=255,blank=True,null=True)
    trade_school= models.CharField(max_length=255,blank=True,null=True)
    graduated_Trade= models.BooleanField(default=False)
    ged= models.BooleanField(default=False)
    list_skills=models.TextField(blank=True,null=True)
    # employment
    name_Of_Employer= models.CharField(max_length=255,blank=True,null=True)
    job_Title= models.CharField(max_length=255,blank=True,null=True)
    date_From=models.DateField(null=True)
    date_To =models.DateField(null=True)
    ok_to_contact= models.BooleanField(default=False)
    contact_number= models.CharField(max_length=10,blank=True,null=True)
    reason_for_leaving= models.CharField(max_length=255,blank=True,null=True)
    # availability
    work_any_Day_Any_Hour= models.BooleanField(default=False)
    work_holidays= models.BooleanField(default=False)
    got_transportation= models.BooleanField(default=False)
    willing_to_travel= models.BooleanField(default=False)
    # schedule
    monday_from=models.CharField(max_length=10,null=True,blank=True)
    monday_to=models.CharField(max_length=10,null=True,blank=True)
    tuesday_from=models.CharField(max_length=10,null=True,blank=True)
    tuesday_to=models.CharField(max_length=10,null=True,blank=True)
    wenesday_from=models.CharField(max_length=10,null=True,blank=True)
    wenesday_to=models.CharField(max_length=10,null=True,blank=True)
    thursday_from=models.CharField(max_length=10,null=True,blank=True)
    thursday_to=models.CharField(max_length=10,null=True,blank=True)
    friday_from=models.CharField(max_length=10,null=True,blank=True)
    friday_to=models.CharField(max_length=10,null=True,blank=True)
    saturday_from=models.CharField(max_length=10,null=True,blank=True)
    saturday_to=models.CharField(max_length=10,null=True,blank=True)
    sunday_from=models.CharField(max_length=10,null=True,blank=True)
    sunday_to=models.CharField(max_length=10,null=True,blank=True)
    disclaimer= models.BooleanField(default=False)

    def __str__(self):
        return self.first_name

    def get_absolute_url(self):
        return reverse('employee:employee_detail', args=[str(self.id)])

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField(blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return self.title



class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    @property
    def get_html_url(self):
        url = reverse('cal:event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'
