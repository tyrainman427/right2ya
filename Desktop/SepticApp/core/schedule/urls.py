from django.urls import path
from . import views

urlpatterns = [
    path('', views.schedule_home, name='schedule_home'),
    path('add/', views.schedule_appointment, name='schedule_appointment'),
    path('api/appointments/', views.appointment_data, name='appointment_data'),
]
