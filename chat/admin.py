from django.contrib import admin
from .models import MessageNotification, Messages, ChatList, AudioMessage, ImageMessage

class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'message', 'timestamp']
    list_filter = ['sender', 'timestamp']
    
    class Meta:
        model = Messages
        
class ChatListAdmin(admin.ModelAdmin):
    list_display = ['user1', 'user2', 'created_at', 'updated_at']
    list_filter = ['user1', 'user2', 'created_at']
    
    class Meta:
        model = ChatList
        
class AudioAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'duration', 'audio_file', 'timestamp']
    list_filter = ['sender']
    
    class Meta:
        model = AudioMessage
        
class ImageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'semantic_autocomplete', 'timestamp']
    list_filter = ['sender', 'receiver']
    readonly_fields = ('semantic_autocomplete',)
    
    class Meta:
        model = ImageMessage
        
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'message', 'read', 'timestamp']
    list_filter = ['sender', 'receiver']
    
    class Meta:
        model = MessageNotification
        
     
admin.site.register(Messages, MessageAdmin)
admin.site.register(ChatList, ChatListAdmin)
admin.site.register(AudioMessage, AudioAdmin)
admin.site.register(ImageMessage, ImageAdmin)
admin.site.register(MessageNotification, NotificationAdmin)