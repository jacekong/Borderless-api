from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)
from django.views.i18n import set_language
from django.views.i18n import JavaScriptCatalog
from . import utils

urlpatterns = [
    path('borderless/admin/', admin.site.urls),
    path('', include('api.urls')),
    path('', include('users.urls')),
    path("api/auth/", include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('', include('friend.urls')),
    path('', include('chat.urls')),
    path('', include('notification.urls')),
    path('i18n/setlang/', set_language, name='set_language'),
    re_path(r'^media/(?P<path>.*)$', utils.serve_media, name='serve_media'),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    
    # social auth
    path('accounts/', include('allauth.urls')),
]
# remove in production
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)


admin.site.site_title = "Borderless admin"
admin.site.site_header = "Borderless admin"
admin.site.index_title = "Admin"
