from django.urls import path
from .views import *
from .routing import websocket_urlpatterns

urlpatterns = [
    path('api/posts', PostsAPIView.as_view()),
    path('api/posts/<str:pk>', PostApiView.as_view()),
    path('api/public/posts/', PublicPostAPIView.as_view()),
    path('api/posts/login/user', CurrentUserPostAPIView.as_view()),
    path('api/post/comments/<str:pk>', PostCommentAPIView.as_view()),
    path('api/check/user/posts/<str:user_id>', SpecificUserPostsAPIView.as_view()),
    
    # web
    path('', Index.as_view(), name='home'),
    path('account/', AccountPage.as_view(), name='account'),
    path('web/post/comments/<str:post>', WebGetPostComments.as_view(), name='web_post_comments'),
    
]

urlpatterns += websocket_urlpatterns