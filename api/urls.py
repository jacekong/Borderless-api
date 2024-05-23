from django.urls import path
from .views import *
from .routing import websocket_urlpatterns

urlpatterns = [
    path('api/posts', PostsAPIView.as_view()),
    path('api/posts/<str:pk>', PostApiView.as_view()),
    path('api/routes', GetRoutesView.as_view()),
    path('api/posts/login/user', CurrentUserPostAPIView.as_view()),
    path('api/post/comments/<str:pk>', PostCommentAPIView.as_view()),
    path('api/check/user/posts/<str:user_id>', SpecificUserPostsAPIView.as_view())
]

urlpatterns += websocket_urlpatterns