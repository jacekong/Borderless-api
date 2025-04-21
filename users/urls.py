from django.urls import path
from .views import UserRegistView, UserSearchAPIView, updateUser, getCurrentUser, UserAuth, logout_user
from .views import WebSearchFriend, WebGetSearchForm, AccountPage
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('user/register/', UserRegistView.as_view(), name='register'),
    path('current/user/', getCurrentUser),
    path('user/update/', updateUser),
    path('api/users/search/', UserSearchAPIView.as_view()),
    
    # web
    path('web/accounts/login/', UserAuth.as_view(), name='login'),
    path('web/accounts/logout/', logout_user, name='logout'),
    path('web/search/friends/', WebGetSearchForm.as_view(), name='search_friend'),
    path('web/search/frined/query/', WebSearchFriend.as_view(), name='search_friend_query'),
    path('web/account/', AccountPage.as_view(), name='account'),
    
    # Password reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt'
    ), name='password_reset'),
    
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
]