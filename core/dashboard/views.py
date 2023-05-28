from core.models import *
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models import Sum, Count, Case, When
from core.views import *
from core.forms import AccountForm, UserForm, MealForm, RestaurantForm
from core.models import Meal, Order, Courier
from django.contrib import messages
from django.db.models import Q

@login_required(login_url="/sign-in/?next=/dashboard/")
def home(request):
    return render(request, 'dashboard/meal.html')

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
  # meals = Meal.objects.filter(restaurant=request.user.restaurant).order_by("-id")
  jobs = Job.objects.filter(customer=request.user.customer).order_by("-id")
  
  return render(request, 'dashboard/meal.html', {
    "jobs": jobs
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
      return redirect(restaurant_meal)

  meal_form = MealForm(instance=Meal.objects.get(id=meal_id))
  return render(request, 'dashboard/edit_meal.html', {
    "meal_form": meal_form
  })

@login_required(login_url='/dashboard/sign_in/')
def dashboard_order(request):
  if request.method == "POST":
    order = Job.objects.get(id=request.POST["id"])
    print(order)
    if order.status == "processing":
       order.status = "ready"
       order.save()
    
    update_templates_and_publish(order.id,order.status)
    
  orders = Job.objects.exclude(Q(status="creating")|Q(status="reviewed")).order_by("-id") #filter(restaurant = request.user.restaurant).order_by("-id") #Order.objects.all().order_by("-id")
  return render(request, 'dashboard/order.html', {
    "orders": orders
  })

@login_required(login_url='/dashboard/sign_in/')
def dashboard_report(request):
  from datetime import datetime, timedelta

  # Calculate the weekdays
  revenue = []
  orders = []
  today = datetime.now()
  current_weekdays = [today + timedelta(days = i) for i in range(0 - today.weekday(), 6 - today.weekday())]

  # print(current_weekdays)

  for day in current_weekdays:
    delivered_orders = Job.objects.filter(status=Job.REVIEWED_STATUS,
      created_at__year = day.year,
      created_at__month = day.month,
      created_at__day = day.day,
    )
  #   delivered_orders = Job.objects.filter(
  #     status = Job.COMPLETED_STATUS,
  #     rated = True,
  #     created_at__year = day.year,
  #     created_at__month = day.month,
  #     created_at__day = day.day,
  #   )
    

  


  revenue.append(sum(order.price for order in delivered_orders))
  orders.append(delivered_orders.count())

  # Getting Top 3 Meals
  top3_meals = Meal.objects.filter(restaurant = request.user.restaurant)\
    .annotate(total_order = Sum('orderdetails__quantity'))\
    .order_by("-total_order")[:3]

  meal = {
    "labels": [meal.name for meal in top3_meals],
    "data": [meal.total_order or 0 for meal in top3_meals]
  }

  # Getting Top 3 Drivers
  top3_drivers = Courier.objects.annotate(
    total_order = Count(
      Case (
        When(order__restaurant = request.user.restaurant, then = 1)
      )
    )
  ).order_by("-total_order")[:3]

  driver = {
    "labels": [d.user.get_full_name() for d in top3_drivers],
    "data": [d.total_order for d in top3_drivers]
  }

  return render(request, 'dashboard/report.html', {
    "revenue": revenue,
    "orders": orders,
    "meal": meal,
    "driver": driver,
  })

