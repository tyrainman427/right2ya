import os
from django.urls import path
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from core.consumers import JobConsumer
from django.core.asgi import get_asgi_application
import core.routing

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fastparcel.settings")
# # Initialize Django ASGI application early to ensure the AppRegistry
# # is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()



application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AuthMiddlewareStack(
            URLRouter([
                path('ws/jobs/<job_id>/', JobConsumer.as_asgi()),
            ])
        ),
    })
