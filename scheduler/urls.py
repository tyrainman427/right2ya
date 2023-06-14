from django.urls import path
from scheduler import views

app_name = 'scheduler'

urlpatterns = [
    # path('create-scheduled-job/', views.create_scheduled_job, name='create_scheduled_job'),
    path('view-scheduled-jobs/', views.view_scheduled_jobs, name='view_scheduled_jobs'),
    path('payment_confirmation/', views.payment_confirmation, name='payment_confirmation'),
    path('create_job/', views.create_job, name='create_job'),
    path('job_confirmation/<uuid:job_id>/', views.job_confirmation, name='job_confirmation'),

]
