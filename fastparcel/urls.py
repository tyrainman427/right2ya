from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from core import views, consumers,apis
from core.views import *

from core.customer import views as customer_views
from core.dashboard import views as dashboard_views
from core.courier import views as courier_views, apis as courier_apis



customer_urlpatterns = [
    path('', customer_views.home, name="home"),
    path('profile/', customer_views.profile_page, name="profile"),
    path('payment_method/', customer_views.payment_method_page, name="payment_method"),
    path('create_job/', customer_views.create_job_page, name="create_job"),
    path('select_job/', customer_views.select_job, name="select_job"),
    path('select-service-type/', customer_views.select_service_type, name='select_service_type'),
    path('choose-meal/', customer_views.choose_meal, name='choose_meal'),
    path('jobs/current/', customer_views.current_jobs_page, name="current_jobs"),
    path('jobs/archived/', customer_views.archived_jobs_page, name="archived_jobs"),
    path('jobs/<uuid:job_id>/', customer_views.job_page, name="job"),
    path('jobs/<uuid:job_id>/add_tip/', customer_views.add_tip, name='add_tip'),
    path('job_summary/<int:job_id>/', customer_views.job_summary, name='job_summary'),
    path('make_payment/<int:job_id>/', customer_views.make_payment, name='make_payment'),
    path('jobs/<uuid:job_id>/cancel_job/', customer_views.cancel_job, name='cancel_job'),
    

]

websocket_urlpatterns = [
    path("ws/jobs/<job_id>/", consumers.JobConsumer.as_asgi()),
]


courier_urlpatterns = [
    path('', courier_views.home, name="home"),
    path('welcome/', courier_views.onboarding_welcome, name="onboarding_welcome"),
    path('onboarding_steps/', courier_views.onboarding_steps, name="onboarding_steps"),
    path('onboarding_safety/', courier_views.onboarding_safety, name="onboarding_safety"),
    path('jobs/available/', courier_views.available_jobs_page, name="available_jobs"),
    path('jobs/available/<id>/', courier_views.available_job_page, name="available_job"),
    path('jobs/current/', courier_views.current_job_page, name="current_job"),
    path('jobs/current/<id>/take_photo/', courier_views.current_job_take_photo_page, name="current_job_take_photo"),
    path('jobs/complete/', courier_views.job_complete_page, name="job_complete"),
    path('jobs/archived/', courier_views.archived_jobs_page, name="archived_jobs"),
    path('profile/', courier_views.profile_page, name="profile"),
    path('payout_method/', courier_views.payout_method_page, name="payout_method"),
    path('save_signature/<uuid:job_id>/', courier_views.save_signature, name='save_signature'),
    path('arrive_at_destination/<uuid:job_id>/', courier_views.arrive_at_destination, name='arrive_at_destination'),
    path('help/', courier_views.help, name="help"),

]

dashboard_urlpatterns = [
    path('meal/', dashboard_views.restaurant_meal, name="restaurant_meal"),
    path('', dashboard_views.dashboard_order, name="dashboard_order"),
    path('report/', dashboard_views.dashboard_report, name="dashboard_report"), 
    path('restaurant/account/', dashboard_views.restaurant_account, name='restaurant_account'),
    path('meal/add/', dashboard_views.restaurant_add_meal, name='restaurant_add_meal'),
    path('meal/edit/<int:meal_id>/', dashboard_views.restaurant_edit_meal, name='restaurant_edit_meal'),
    path('available/', dashboard_views.available_drivers, name="available_drivers"),
    path('all_jobs/', dashboard_views.all_jobs_page, name="all_jobs"),
    path('job/<uuid:pk>/', dashboard_views.JobDetailView.as_view(), name='job_detail'),
    path('all_jobs/archived', dashboard_views.all_archived_jobs_page, name="all_archived_jobs"),
    path('job/<uuid:pk>/edit/', dashboard_views.JobEditView.as_view(), name='edit_job'),

]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('payout/', views.admin_payout, name='admin_payout'),
    path('driver_signup/', views.driver_signup, name='driver_signup'),

    path('update-switch-state/', courier_views.update_switch_state, name='update_switch_state'),
    path('rate-courier/<uuid:job_id>/', views.rate_courier, name='rate_courier'),

    # path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',  
    #     activate, name='activate'),  
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),  
    
    
    path('sign-in/', auth_views.LoginView.as_view(template_name="sign_in.html")),
    path('sign-out/', auth_views.LogoutView.as_view(next_page="/")),
    path('sign-up/', views.sign_up),
    
    path('customer/', include((customer_urlpatterns, 'customer'))),
    path('courier/', include((courier_urlpatterns, 'courier'))),
    path('dashboard/', include((dashboard_urlpatterns, 'dashboard'))),
    path('firebase-messaging-sw.js', (TemplateView.as_view(template_name="firebase-messaging-sw.js", content_type="application/javascript",))),
    
    
    # ------------------------ APIS -------------------------
    
    path('api/customer/restaurants/', apis.customer_get_restaurants),
    path('api/customer/meals/<int:restaurant_id>', apis.customer_get_meals),
    path('api/customer/order/add/', apis.customer_add_order),
    path('api/customer/order/latest/', apis.customer_get_latest_order),
    path('api/customer/order/latest_status/', apis.customer_get_latest_order_status),
    path('api/customer/driver/location/', apis.customer_get_driver_location),
    path('api/customer/payment_intent/', apis.create_payment_intent),
    path('api/dashboard/order/notification/', apis.restaurant_order_notification),
    path('api/notification/<int:notification_id>/read/', apis.mark_notification_as_read, name='mark_notification_as_read'),

    path('api/jobs/available/', courier_views.JobList.as_view(), name="jobs_api"),
    path('api/jobs/current/<id>/update/', courier_apis.current_job_update_api, name="current_job_update_api"),
    path('api/fcm-token/update/', courier_apis.fcm_token_update_api, name="fcm_token_update_api"),
    
    path('api/driver/order/ready/', apis.driver_get_ready_orders),
    path('api/driver/order/pick/', apis.driver_pick_order),
    path('api/driver/order/latest/', apis.driver_get_latest_order),
    path('api/driver/order/complete/', apis.driver_complete_order),
    path('api/driver/revenue/', apis.driver_get_revenue),
    path('api/driver/location/update/', apis.driver_update_location),
    path('api/driver/profile/', apis.driver_get_profile),
    path('api/driver/profile/update/', apis.driver_update_profile),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
