from channels.db import database_sync_to_async
from users.models import CustomUser
from jwt import InvalidTokenError, ExpiredSignatureError
import jwt
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.authentication import BaseAuthentication

class JWTAuthentication(BaseAuthentication):
    
    @database_sync_to_async
    def authenticate_user(self, scope, token):
        # print(f'-------------token: {token}--------------')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            user = CustomUser.objects.get(id=user_id)
            return user
        except (InvalidTokenError, ExpiredSignatureError , CustomUser.DoesNotExist):
            raise AuthenticationFailed("Invalid token")