from django.urls import path
from .views import SendFriendRequest, AcceptFriendRequest, DeclineFriendRequest, CancelFriendRequest, RemoveFriend, UserFriendsAPIView, UserFriendsRequestList

urlpatterns = [
    path('send/friend/request/', SendFriendRequest.as_view(), name='send_friend_request'),
    path('accept/friend/request/', AcceptFriendRequest.as_view(), name='accept_friend_request'),
    path('decline/friend/request/', DeclineFriendRequest.as_view(), name='decline_friend_request'),
    path('cancel/friend/request/', CancelFriendRequest.as_view(), name='cancel_friend_request'),
    path('remove/friend/', RemoveFriend.as_view(), name='remove_friend'),
    path('api/user/friends/', UserFriendsAPIView.as_view(), name='user_friends'),
    path('api/user/friend/request/', UserFriendsRequestList.as_view(), name='user_friend')
]
