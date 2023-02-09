from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from core import apis

from core import views, consumers

from core.customer import views as customer_views
from core.dashboard import views as dashboard_views
from core.courier import views as courier_views, apis as courier_apis

customer_urlpatterns = [
    path('', customer_views.home, name="home"),
    path('profile/', customer_views.profile_page, name="profile"),
    path('payment_method/', customer_views.payment_method_page, name="payment_method"),
    path('create_job/', customer_views.create_job_page, name="create_job"),

    path('jobs/current/', customer_views.current_jobs_page, name="current_jobs"),
    path('jobs/archived/', customer_views.archived_jobs_page, name="archived_jobs"),
    path('jobs/<job_id>/', customer_views.job_page, name="job"),
]

courier_urlpatterns = [
    path('', courier_views.home, name="home"),
    path('jobs/available/', courier_views.available_jobs_page, name="available_jobs"),
    path('jobs/available/<id>/', courier_views.available_job_page, name="available_job"),
    path('jobs/current/', courier_views.current_job_page, name="current_job"),
    path('jobs/current/<id>/take_photo/', courier_views.current_job_take_photo_page, name="current_job_take_photo"),
    path('jobs/complete/', courier_views.job_complete_page, name="job_complete"),
    path('jobs/archived/', courier_views.archived_jobs_page, name="archived_jobs"),
    path('profile/', courier_views.profile_page, name="profile"),
    path('payout_method/', courier_views.payout_method_page, name="payout_method"),

    path('api/jobs/available/', courier_apis.available_jobs_api, name="available_jobs_api"),
    path('api/jobs/current/<id>/update/', courier_apis.current_job_update_api, name="current_job_update_api"),
    path('api/fcm-token/update/', courier_apis.fcm_token_update_api, name="fcm_token_update_api"),
]

dashboard_urlpatterns = [
    path('', dashboard_views.home, name="dashboard_home"),
    path('service/', dashboard_views.dashboard_service, name="dashboard_service"),
    path('service/add-service', dashboard_views.dashboard_add_service, name="dashboard_add_service"),
    path('order/', dashboard_views.dashboard_order, name="dashboard_order"),
    path('report/', dashboard_views.dashboard_report, name="dashboard_report"),
    path('service/edit/<int:service_id>', dashboard_views.company_edit_service, name='company_edit_service'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('privacy/',privacy, name="privacy"),
    path('', include('social_django.urls', namespace='social')),
    path('', views.home),
    
    # Web View - Restaurant
    path('sign-in/', auth_views.LoginView.as_view(template_name="sign_in.html")),
    path('sign-out/', auth_views.LogoutView.as_view(next_page="/")),
    path('sign-up/', views.sign_up),
    # path('restaurant/', views.restaurant_home, name='restaurant_home'),
    

    
    
    path('customer/', include((customer_urlpatterns, 'customer'))),
    path('courier/', include((courier_urlpatterns, 'courier'))),
    path('dashboard/', include((dashboard_urlpatterns, 'dashboard'))),
    path('firebase-messaging-sw.js', (TemplateView.as_view(template_name="firebase-messaging-sw.js", content_type="application/javascript",))),
    
     # APIs
    #  /convert-token (sign-in/sign-up), /revoke-token (sign-out)
    path('api/social/', include('rest_framework_social_oauth2.urls')),
    path('api/dashboard/order/notification/<last_request_time>/', apis.company_order_notification),

    # APIS for CUSTOMERS
    # path('api/customer/restaurants/', apis.customer_get_restaurants),
    path('api/dashboard/services/', apis.customer_get_services),
    path('api/dashboard/order/add/', apis.customer_add_order),
    path('api/dashboard/order/latest/', apis.customer_get_latest_order),
    path('api/dashboard/order/latest_status/', apis.customer_get_latest_order_status),
    path('api/dashboard/driver/location/', apis.customer_get_driver_location),
    path('api/customer/payment_intent/', apis.create_payment_intent),

    # APIS for DRIVERS
    path('api/driver/order/ready/', apis.driver_get_ready_orders),
    path('api/driver/order/pick/', apis.driver_pick_order),
    path('api/driver/order/latest/', apis.driver_get_latest_order),
    path('api/driver/order/complete/', apis.driver_complete_order),
    path('api/driver/revenue/', apis.driver_get_revenue),
    path('api/driver/location/update/', apis.driver_update_location),
    path('api/driver/profile/', apis.driver_get_profile),
    path('api/driver/profile/update/', apis.driver_update_profile),
]

websocket_urlpatterns = [
    url(r'^ws/jobs/(?P<job_id>[^/]+)/$', consumers.JobConsumer.as_asgi())
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
