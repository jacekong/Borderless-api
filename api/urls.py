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
    path('web/post/comments/<str:post>', WebGetPostComments.as_view(), name='web_post_comments'),
    path('web/post/detail/<str:post_id>', WebPostDetail.as_view(), name='web_post_detail'),
    path('web/post/create', WebRenderCreatePostTemplate.as_view(), name='web_post_creation'),
    path('web/post/<str:post_id>/like/', LikePostView.as_view(), name='toggle_like'),
    path('web/post/<str:post_id>/comment/', WebLoadCommentsView.as_view(), name='comments_list'),
]

urlpatterns += websocket_urlpatterns