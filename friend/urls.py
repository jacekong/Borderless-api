from django.urls import path
from .views import SendFriendRequest, AcceptFriendRequest, DeclineFriendRequest, CancelFriendRequest, RemoveFriend, UserFriendsAPIView, UserFriendsRequestList
from .views import WebSendFriendRequest

urlpatterns = [
    path('send/friend/request/', SendFriendRequest.as_view()),
    path('accept/friend/request/', AcceptFriendRequest.as_view()),
    path('decline/friend/request/', DeclineFriendRequest.as_view()),
    path('cancel/friend/request/', CancelFriendRequest.as_view()),
    path('remove/friend/', RemoveFriend.as_view()),
    path('api/user/friends/', UserFriendsAPIView.as_view()),
    path('api/user/friend/request/', UserFriendsRequestList.as_view()),
    
    
    # web
    path('web/send/friend/request', WebSendFriendRequest.as_view(), name='send_friend_request'),
]
