from channels.middleware import BaseMiddleware
from django.conf import settings
import jwt
from rest_framework.exceptions import AuthenticationFailed
from django.db import close_old_connections
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from users.models import CustomUser
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.sessions.models import Session
from django.core.exceptions import ObjectDoesNotExist

class JWTAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        self.inner = inner
            
    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])

        if b'authorization' in headers:
            try:
                token_name, token = headers[b'authorization'].decode().split()
                if token_name == 'Bearer':
                    user = await self.authenticate_user(token)
                    if user is not None:
                        scope['user'] = user
                        close_old_connections()
                    else:
                        scope['user'] = AnonymousUser()
            except (InvalidTokenError, AuthenticationFailed):
                raise AuthenticationFailed("Invalid token")
        
        if b'cookie' in headers:
            cookies = headers[b'cookie'].split(b'; ')
            for cookie in cookies:
                if cookie.startswith(b'sessionid='):
                    sessionid = cookie.split(b'=')[1].decode()
                    break

        if sessionid:
            user = await self.authenticate_session(sessionid)
            if user is not None:
                scope['user'] = user
            else:
                scope['user'] = AnonymousUser()
        else:
            scope['user'] = AnonymousUser()

        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def authenticate_user(self, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            user = CustomUser.objects.get(id=user_id)
            return user
        except (InvalidTokenError, ExpiredSignatureError , CustomUser.DoesNotExist):
            raise AuthenticationFailed("Invalid token")
        
    @database_sync_to_async
    def authenticate_session(self, sessionid):
        try:
            session = Session.objects.get(session_key=sessionid)
            userid = session.get_decoded().get('_auth_user_id')
            user = CustomUser.objects.get(id=userid)
            return user if user is not None and user.is_authenticated else None
        except (ObjectDoesNotExist, KeyError):
            return None