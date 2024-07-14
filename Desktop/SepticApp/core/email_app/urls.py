from django.urls import path
from . import views

urlpatterns = [
    path('send-email/<int:contact_id>/<int:property_id>/', views.send_invoice_email, name='send_email'),
    path('', views.email_list, name='email_list'),
]
