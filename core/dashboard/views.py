from core.models import *
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models import Sum, Count, Case, When
from core.views import *
from core.forms import AccountForm, UserForm, MealForm, RestaurantForm
from core.models import Meal, Order, Courier, Notification
from django.contrib import messages
from django.db.models import Q
from datetime import datetime, timedelta
from django.http import HttpResponseRedirect, JsonResponse
import json
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from core.models import Job
from django.conf import settings
from datetime import date


@login_required(login_url="/sign-in/?next=/dashboard/")
def home(request):   
    return render(request, 'dashboard/order.html')

@login_required(login_url='/restaurant/sign_in/')
def restaurant_account(request):

  if request.method == "POST":
    account_form = AccountForm(request.POST, instance=request.user)
    restaurant_form = RestaurantForm(request.POST, request.FILES, instance=request.user.restaurant)

    if account_form.is_valid() and restaurant_form.is_valid():
      account_form.save()
      restaurant_form.save()

  account_form = AccountForm(instance=request.user)
  restaurant_form = RestaurantForm(instance=request.user.restaurant)

  return render(request, 'dashboard/account.html', {
    "account_form": account_form,
    "restaurant_form": restaurant_form
  })

@login_required(login_url='/dashboard/sign_in/')
def restaurant_meal(request):
  meals = Meal.objects.filter(restaurant=request.user.restaurant).order_by("-id")
  jobs = Job.objects.filter(customer=request.user.customer).order_by("-id")
  
  return render(request, 'dashboard/meal.html', {
    "jobs": jobs,
    "meals":meals,
  })

@login_required(login_url='/dashboard/sign_in/')
def restaurant_add_meal(request):

  if request.method == "POST":
    meal_form = MealForm(request.POST, request.FILES)

    if meal_form.is_valid():
      meal = meal_form.save(commit=False)
      meal.restaurant = request.user.restaurant
      meal.save()
      return redirect(reverse('dashboard:restaurant_meal'))

  meal_form = MealForm()
  return render(request, 'dashboard/add_meal.html', {
    "meal_form": meal_form
  })


@login_required(login_url='/dashboard/sign_in/')
def restaurant_edit_meal(request, meal_id):

  if request.method == "POST":
    meal_form = MealForm(request.POST, request.FILES, instance=Meal.objects.get(id=meal_id))

    if meal_form.is_valid():
      meal_form.save()
      return HttpResponseRedirect(reverse('dashboard:restaurant_meal'))

  meal_form = MealForm(instance=Meal.objects.get(id=meal_id))
  return render(request, 'dashboard/edit_meal.html', {
    "meal_form": meal_form
  })

@login_required(login_url='/dashboard/sign_in/')
def dashboard_order(request):
    
    if request.method == "POST":
        order = Job.objects.get(id=request.POST["id"])
        notification = Notification.objects.filter(job=order).first()

        if notification:
            notification.read = True
            notification.save()
        else:
            print("No notification found for this job.")
            

        if order.status == "processing":
            order.status = "ready"
            order.save()
        elif order.status == "scheduled":
            order.status = "ready"
            order.save()
            

            if notification:  # Check if notification is not None before accessing its attributes
                notification.read = True
                notification.save()

    # today = timezone.localdate()
    all_jobs = Job.objects.exclude(Q(status="creating")|Q(status="reviewed")|Q(status="completed")|Q(is_scheduled=True)).order_by("-id")
    # orders = [job for job in all_jobs if not job.is_scheduled or job.scheduled_date.date() <= today]
    
    today = date.today()

    # Fetch orders that are scheduled for today
    scheduled_orders = Job.objects.filter(is_scheduled=True)

    context = {
        'immediate_orders': all_jobs,
        'scheduled_orders': scheduled_orders,
        'today': today,
    }
    
    return render(request, 'dashboard/order.html',context)


@login_required(login_url='/dashboard/sign_in/')
def dashboard_report(request):
    # Calculate the weekdays
    revenue = []
    orders = []
    today = datetime.now()
    current_weekdays = [today + timedelta(days=i) for i in range(0 - today.weekday(), 6 - today.weekday())]

    for day in current_weekdays:
        delivered_orders = Job.objects.filter(
            status__in=[Job.COMPLETED_STATUS, Job.REVIEWED_STATUS],
            created_at__year=day.year,
            created_at__month=day.month,
            created_at__day=day.day,
        )

        revenue.append(sum(order.price for order in delivered_orders))
        orders.append(delivered_orders.count())
    # Convert all Decimal to float
    revenue = [float(x) for x in revenue]

    print("Revenue:", revenue)

    
    
    # Getting Top 3 Customers
    top3_customers = Customer.objects.annotate(
        total_order=Count('order')
    ).order_by("-total_order")[:3]

    customer = {
        "labels": [c.user.get_full_name() for c in top3_customers],
        "data": [c.total_order for c in top3_customers]
    }

    # Getting Top 3 Drivers
    top3_drivers = Customer.objects.annotate(
        total_order=Count(
            Case(
                When(order__customer=request.user.customer, then=1)
            )
        )
    ).order_by("-total_order")[:3]

    driver = {
        "labels": [d.user.get_full_name() for d in top3_drivers],
        "data": [d.total_order for d in top3_drivers]
    }


    return render(request, 'dashboard/report.html', {
        "revenue_json": json.dumps(revenue),

        "revenue": revenue,
        "orders": orders,
        "customer": customer,  # Pass the customer data
        "driver": driver,
    })


@login_required(login_url='/dashboard/sign_in/')
def available_drivers(request):
    all_drivers = Courier.objects.all()
    available_drivers = [driver for driver in all_drivers if driver.is_available and not driver.on_job()]
    unavailable_drivers = [driver for driver in all_drivers if not driver.is_available]
    on_job_drivers = [driver for driver in all_drivers if driver.is_available and driver.on_job()]

    return render(request, 'dashboard/available_drivers.html', {
        "available_drivers": available_drivers,
        'unavailable_drivers': unavailable_drivers,
        'on_job_drivers': on_job_drivers,
    })


def get_latest_job_statuses(request):
    try:
        jobs = Job.objects.all().values('id', 'status')  # Replace 'status' with the actual field name for the job status
        job_list = list(jobs)
        return JsonResponse({'status': 'success', 'data': job_list})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


@login_required(login_url="/sign-in/?next=/customer/")
def all_jobs_page(request):
    current_date = timezone.localtime().date()
    query = request.GET.get('q', '')
    jobs = Job.objects.filter(
        customer=request.user.customer,
        status__in=[
            Job.PROCESSING_STATUS,
            Job.READY_STATUS,
            Job.PICKING_STATUS,
            Job.DELIVERING_STATUS,
            Job.SCHEDULED_STATUS
        ]
    ).filter(
        Q(scheduled_date=current_date, service_type='scheduled') |
        Q(service_type='standard') |
        Q(name__icontains=query) |
        Q(id__icontains=query) |
        Q(status__icontains=query)
    )

    return render(request, 'dashboard/all_jobs.html', {
        "jobs": jobs,
    })

@login_required(login_url="/sign-in/?next=/customer/")
def all_archived_jobs_page(request):
    jobs = Job.objects.filter(
        status__in=[
            Job.COMPLETED_STATUS,
            Job.CANCELED_STATUS,
            Job.REVIEWED_STATUS
        ]
    )
  
    return render(request, 'dashboard/all_jobs.html', {
        "jobs": jobs,

    })



class JobDetailView(DetailView):
    model = Job
    template_name = 'dashboard/job_detail.html'
    context_object_name = 'job'  # This should be a string

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['GOOGLE_MAP_API_KEY'] = settings.GOOGLE_MAP_API_KEY
        return context
      
class JobEditView(UpdateView):
    model = Job
    template_name = 'dashboard/edit_job.html'
    fields = ['customer', 'courier','name','description','category','size','quantity','photo', 'status','pickup_name','pickup_address',"pickup_phone",'delivery_address','delivery_name','delivery_phone','pickup_photo','delivery_photo','delivered_at']
    success_url = reverse_lazy('dashboard:all_jobs')