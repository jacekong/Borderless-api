from django.contrib import admin
from notification.models import Notification

class NotificationAdmin(admin.ModelAdmin):
    list_filter = ['user', 'message', 'type', 'sender']
    list_display = ['sender', 'message', 'user', 'type', 'created_at', 'related_link', 'is_read', 'is_sent']
    search_fields = ['user__username', 'user__email', 'message']
    
    class Meta:
        model = Notification
        
admin.site.register(Notification, NotificationAdmin)