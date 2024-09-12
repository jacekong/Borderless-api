from django.urls import path
from .views import UserRegistView, UserSearchAPIView, updateUser, getCurrentUser, UserAuth, logout_user
from .views import WebSearchFriend, WebGetSearchForm

urlpatterns = [
    path('user/register/', UserRegistView.as_view()),
    path('current/user/', getCurrentUser),
    path('user/update/', updateUser),
    path('api/users/search/', UserSearchAPIView.as_view()),
    
    # web
    path('web/accounts/login/', UserAuth.as_view(), name='login'),
    path('web/accounts/logout/', logout_user, name='logout'),
    path('web/search/friends/', WebGetSearchForm.as_view(), name='search_friend'),
    path('web/search/frined/query/', WebSearchFriend.as_view(), name='search_friend_query'),
]