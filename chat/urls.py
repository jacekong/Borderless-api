from django.urls import path
from .views import (AudioChatHistoryAPIView, 
                    GetChatHistoryAPIView, 
                    ChatListAPIView, 
                    ChatListCreateView,
                    ImageMessageCreateAPIView,
                    ImageMessageHistoryAPIView,
                    get_notification
                    )
from .routing import websocket_urlpatterns

from chat.views import ChatWebPage, ChatAreaWebView

urlpatterns = [
    path('api/chat/history/<str:user_id>/', GetChatHistoryAPIView.as_view()),
    path('api/chat/history/images/<str:user_id>/', ImageMessageHistoryAPIView.as_view()),
    path('api/chatlists/', ChatListAPIView.as_view()),
    path('api/chatlist/create/', ChatListCreateView.as_view()),
    path('api/chat/images/', ImageMessageCreateAPIView.as_view()),
    path('api/chat/history/voice/<str:user_id>/', AudioChatHistoryAPIView.as_view()),
    path('api/notification/', get_notification),
    
    
    # web
    path('web/chat/page/', ChatWebPage.as_view(), name='chat_page'),
    path('web/chat/user/<str:user_id>/', ChatAreaWebView.as_view(), name='chat_with_user')
]

urlpatterns += websocket_urlpatterns
