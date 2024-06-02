from django.urls import path
from .views import *

app_name = 'newContract'

urlpatterns = [
    path('', index,name='home'),
    path('contract/', contract, name="contract"),
    path('contract/<pk>', ContractDetailView.as_view(), name="contract_detail")
]
