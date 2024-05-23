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

class JWTAuthMiddleware(BaseMiddleware):
    # def __init__(self, inner):
    #     self.inner = inner
        
    # async def __call__(self, scope, receive, send):
    #     close_old_connections()
        
    #     # Extract the JWT token from the query parameters or headers
    #     query_string = scope.get('query_string', b'').decode('utf-8')
    #     query_parameters = dict(qp.split('=') for qp in query_string.split('&'))
    #     token = query_parameters.get('token', None)
        
    #     if token is None:
    #         await send({
    #             'type': 'websocket.close',
    #             'code': 4000
    #         })
            
    #     authentication = JWTAuthentication()
        
    #     try:
    #         user = await authentication.authenticate_user(scope, token)
    #         # print(f'------- user {user} --------')
    #         if user is not None:
    #             scope['user'] = user
    #         else:
    #             await send({
    #                 'type': 'websocket.close',
    #                 'code': 4000
    #             })
            
    #         return await super().__call__(scope, receive, send)
    #     except AuthenticationFailed:
    #         await send({
    #             'type': 'websocket.close',
    #             'code': 4002
    #         })
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
