
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from customer.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('restaurant/', include('restaurant.urls')),
    path('', Index.as_view(), name="index"),
    path('about/', About.as_view(), name="about"),
    path('order/', Order.as_view(), name="order"),
    path('order-confirmation/<int:pk>', OrderConfirmation.as_view(), name="order-confirmation"),
    path('payment-confirmation/', OrderPayConfirmation.as_view(), name="payment-confirmation"),
    
    path('menu/', Menu.as_view(),name='menu'),
    path('menu/search', MenuSearch.as_view(),name="menu-search")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
