from django.urls import path
from core.consumers import JobConsumer

websocket_urlpatterns = [
    path("ws/jobs/<job_id>/", JobConsumer.as_asgi()),
]