from django.urls import path
from .import views

urlpatterns = [
    path('', views.work_order_list, name='work_order_list'),
    path('create/', views.create_work_order, name='create_work_order'),
    path('ajax/load-properties/', views.ajax_load_properties, name='ajax_load_properties'),
    path('<int:order_id>/', views.work_order_detail, name='work_order_detail'),
    path('<int:order_id>/complete/', views.complete_work_order, name='complete_work_order'),
    path('<int:order_id>/create_invoice/', views.create_invoice_from_work_order, name='create_invoice_from_work_order'),


]