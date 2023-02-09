from core.models import *
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models import Sum, Count, Case, When

from core.dashboard.forms import ServiceForm
from core.models import Service, Order, Courier


@login_required(login_url="/sign-in/?next=/dashboard/")
def home(request):
    return render(request, 'dashboard/home.html')

# @login_required(login_url='/restaurant/sign_in/')
# def restaurant_account(request):

#   if request.method == "POST":
#     account_form = AccountForm(request.POST, instance=request.user)
#     restaurant_form = RestaurantForm(request.POST, request.FILES, instance=request.user.restaurant)

#     if account_form.is_valid() and restaurant_form.is_valid():
#       account_form.save()
#       restaurant_form.save()

#   account_form = AccountForm(instance=request.user)
#   restaurant_form = RestaurantForm(instance=request.user.restaurant)

#   return render(request, 'restaurant/account.html', {
#     "account_form": account_form,
#     "restaurant_form": restaurant_form
#   })

@login_required(login_url='/dashboard/sign_in/')
def dashboard_service(request):

  services = Service.objects.all()  #filter(dashboard=request.user.customer).order_by("-id")
  return render(request, 'dashboard/meal.html', {
    "services": services
  })

@login_required(login_url='/customer/sign_in/')
def dashboard_add_service(request):

  if request.method == "POST":
    service_form = ServiceForm(request.POST, request.FILES)

    if service_form.is_valid():
      service = service_form.save(commit=False)
      service.dashboard = request.user.customer
      service.save()
      return redirect('dashboard:dashboard_service')

  service_form = ServiceForm()
  return render(request, 'dashboard/add_meal.html', {
    "service_form": service_form
  })

@login_required(login_url='/dashboard/sign_in/')
def company_edit_service(request, service_id):

  if request.method == "POST":
    service_form = ServiceForm(request.POST, request.FILES, instance=Service.objects.get(id=service_id))

    if service_form.is_valid():
      service_form.save()
      return redirect("/dashboard/service/")

  service_form = ServiceForm(instance=Service.objects.get(id=service_id))
  return render(request, 'dashboard/edit_meal.html', {
    "meal_form": service_form
  })

@login_required(login_url='/dashboard/sign_in/')
def dashboard_order(request):
  if request.method == "POST":
    order = Order.objects.get(id=request.POST["id"])

    if order.status == Order.PROCESSING:
      order.status = Order.READY
      order.save()

  orders = Order.objects.filter(restaurant = request.user.restaurant).order_by("-id")
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
  current_weekdays = [today + timedelta(days = i) for i in range(0 - today.weekday(), 7 - today.weekday())]

  # print(current_weekdays)

  for day in current_weekdays:
    delivered_orders = Order.objects.filter(
      status = Order.DELIVERED,
      created_at__year = day.year,
      created_at__month = day.month,
      created_at__day = day.day,
    )

    revenue.append(sum(order.total for order in delivered_orders))
    orders.append(delivered_orders.count())

  # Getting Top 3 Meals
    top3_services = Service.objects.all() #filter(dashboard = request.user.customer)\
    Service.total_order = Sum('orderdetails__quantity')
#     .order_by("-total_order")[:3]

  services = {
    "labels": [service.name for service in top3_services],
    "data": [service.total_order or 0 for service in top3_services]
  }

  # Getting Top 3 Drivers
#   top3_drivers = Courier.objects.annotate(
#     total_order = Count(
#       Case (
#         When(order__dashboard = request.user, then = 1)
#       )
#     )
#   ).order_by("-total_order")[:3]

#   driver = {
#     "labels": [d.user.get_full_name() for d in top3_drivers],
#     "data": [d.total_order for d in top3_drivers]
#   }

  return render(request, 'dashboard/report.html', {
    "revenue": revenue,
    "orders": orders,
    "services": services,
    # "driver": driver,
  })

