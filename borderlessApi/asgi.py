
import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from chat.channel_middlware import JWTAuthMiddleware
import chat.routing
import api.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'borderlessApi.settings')

websocket_urlpatterns = chat.routing.websocket_urlpatterns + api.routing.websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
            JWTAuthMiddleware(
                AuthMiddlewareStack(
                    URLRouter(
                        websocket_urlpatterns,
                    )
                )
            )
        ),
})
