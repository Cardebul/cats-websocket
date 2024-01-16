"""
ASGI config for service project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import logging
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'service.settings')

application = get_asgi_application()



django_asgi_app = get_asgi_application()
from app.routing import websocket_urlpatterns
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator



from channels.auth import AuthMiddlewareStack

from logging import info as i

logger = logging.getLogger(__name__)

class TokenAuthMiddleware:
    """Token authorization"""

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope, *args, **kwargs):
        try:
            
            params = scope.get('query_string')
            params = params.decode() if isinstance(params, bytes) else params
            
            token = params.split('=')[1]
            i(token)
            scope['user_token'] = token
        except Exception:
            pass
        room_id = scope["path"].split('/')
        room_id = room_id[-1] if room_id[-1] != '' else room_id[-2]
        scope['user_id'] = room_id
        return self.inner(scope, *args, **kwargs)    

TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            TokenAuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        ),
    }
)

