
from channels.auth import AuthMiddlewareStack


class TokenAuthMiddleware:
    """Token authorization"""

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope, *args, **kwargs):
        try:
            params = scope.get('query_string')
            params = params.decode() if isinstance(params, bytes) else params

            token = params.split('=')[1]
            scope['user_token'] = token
        except Exception:
            pass
        room_id = scope["path"].split('/')
        room_id = room_id[-1] if room_id[-1] != '' else room_id[-2]
        scope['user_id'] = room_id
        return self.inner(scope, *args, **kwargs)


def TokenAuthMiddlewareStack(inner): return TokenAuthMiddleware(
    AuthMiddlewareStack(inner))
