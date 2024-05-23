from django.urls import path
from .views import UserRegistView, UserSearchAPIView, updateUser, getCurrentUser

urlpatterns = [
    path('user/register/', UserRegistView.as_view(), name='register'),
    path('current/user/', getCurrentUser, name='current_user'),
    path('user/update/', updateUser, name='update'),
    path('api/users/search/', UserSearchAPIView.as_view(), name='user_search'),
]