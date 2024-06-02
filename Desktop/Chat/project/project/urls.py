from django.contrib import admin
from django.urls import path
from app.views import chat_box, index

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="index"),
    path("chat/<str:room_name>/", chat_box, name="room"),
]