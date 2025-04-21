from django.urls import path
from .views import SendFriendRequest, AcceptFriendRequest, DeclineFriendRequest, CancelFriendRequest, RemoveFriend, UserFriendsAPIView, UserFriendsRequestList
from .views import WebSendFriendRequest,WebFriendList,WebFriendDetail,WebAcceptFriendRequest

urlpatterns = [
    path('send/friend/request/', SendFriendRequest.as_view()),
    path('accept/friend/request/', AcceptFriendRequest.as_view()),
    path('decline/friend/request/', DeclineFriendRequest.as_view()),
    path('cancel/friend/request/', CancelFriendRequest.as_view()),
    path('remove/friend/', RemoveFriend.as_view()),
    path('api/user/friends/', UserFriendsAPIView.as_view()),
    path('api/user/friend/request/', UserFriendsRequestList.as_view()),
    
    
    # web
    path('web/send/friend/request/<str:user_id>', WebSendFriendRequest.as_view(), name='send_friend_request'),
    path('web/friend/list/', WebFriendList.as_view(), name='friend_list'),
    path('web/friend/detail/<str:post_author>', WebFriendDetail.as_view(), name='friend_detail'),
    path('web/accept/<str:user_id>/request/', WebAcceptFriendRequest.as_view(), name='accept_friend_request'),
]
