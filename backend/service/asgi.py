"""
THE IMPORTS MUST BE IN THIS ORDER, DO NOT CHANGE ANYTHING IN THIS FILE
"""

import logging
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'service.settings')




django_asgi_app = get_asgi_application()
from logging import info as i

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from app.routing import websocket_urlpatterns
from.mdlwr import TokenAuthMiddlewareStack
logger = logging.getLogger(__name__)



application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            TokenAuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        ),
    }
)

