import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import core.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fastparcel.settings")
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()



application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": 
            AuthMiddlewareStack(URLRouter(core.routing.websocket_urlpatterns))
        ,
    }
)